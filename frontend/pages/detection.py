import streamlit as st
import io
import os
import time
from datetime import datetime
from PIL import Image

from frontend.components.cards import render_top_header, render_workflow_steps, render_disclaimer, render_footer
from frontend.components.sample_selector import render_sample_selector, get_verified_samples
from frontend.components.result_panel import render_result_panel
from frontend.services.api_client import get_api_client

def render_detection_page(is_api_connected: bool):
    """
    Render modernized MRI Analysis workspace with 4-step workflow, visual sample cards,
    scanning loading animation, and comprehensive results panel.
    """
    # Determine current workflow step
    current_step = 1
    if "last_pred" in st.session_state:
        current_step = 3
    elif "last_bytes" in st.session_state:
        current_step = 2

    render_top_header(
        title="Brain MRI Detection & Analysis",
        description="Upload a patient cranial MRI scan to detect and classify brain tumors using YOLOv8 computer vision.",
        meta_text="Model: YOLOv8n • Inference: Dual-Mode (FastAPI / In-Process Fallback)",
        badges=["YOLOv8 Detection", "Sub-Second Latency", "Export Ready"]
    )

    render_workflow_steps(current_step=current_step)

    col_left, col_right = st.columns([1.1, 1.9], gap="large")

    # Handle auto-load sample from Dashboard CTA
    if st.session_state.get("auto_load_sample", False):
        samples = get_verified_samples()
        if samples:
            with open(samples[0]["path"], "rb") as f:
                st.session_state["last_bytes"] = f.read()
                st.session_state["last_filename"] = os.path.basename(samples[0]["path"])
        st.session_state["auto_load_sample"] = False

    with col_left:
        st.markdown("### 1. Upload MRI Scan")
        
        uploaded_file = st.file_uploader(
            "Drop MRI scan here (or click to browse)",
            type=["png", "jpg", "jpeg"],
            help="Supported formats: PNG, JPG, JPEG (Max 15MB)",
            label_visibility="collapsed"
        )

        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

        # Visual sample selector
        selected_sample_path = render_sample_selector()
        if selected_sample_path:
            with open(selected_sample_path, "rb") as f:
                st.session_state["last_bytes"] = f.read()
                st.session_state["last_filename"] = os.path.basename(selected_sample_path)
            if "last_pred" in st.session_state:
                del st.session_state["last_pred"]
            st.rerun()

        st.markdown("---")
        st.markdown("### 2. Inference Settings")
        
        conf_threshold = st.slider(
            "Detection Confidence Threshold",
            min_value=0.10,
            max_value=0.95,
            value=0.50,
            step=0.05,
            help="Minimum certainty percentage for bounding boxes to be considered positive detections."
        )

        st.markdown("""
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: -8px; margin-bottom: 16px;">
                Higher values reduce false positives; lower values increase sensitivity.
            </div>
        """, unsafe_allow_html=True)

        # Determine active image bytes
        active_bytes = None
        active_filename = ""

        if uploaded_file is not None:
            active_bytes = uploaded_file.getvalue()
            active_filename = uploaded_file.name
            st.session_state["last_bytes"] = active_bytes
            st.session_state["last_filename"] = active_filename
        elif "last_bytes" in st.session_state:
            active_bytes = st.session_state["last_bytes"]
            active_filename = st.session_state.get("last_filename", "mri_scan.jpg")

        can_analyze = active_bytes is not None
        run_analysis = st.button(
            "🚀 Run Tumor Detection",
            type="primary",
            disabled=not can_analyze,
            use_container_width=True
        )

        if can_analyze:
            if st.button("🔄 Clear Current Scan", use_container_width=True, type="secondary"):
                if "last_bytes" in st.session_state:
                    del st.session_state["last_bytes"]
                if "last_filename" in st.session_state:
                    del st.session_state["last_filename"]
                if "last_pred" in st.session_state:
                    del st.session_state["last_pred"]
                st.rerun()

    with col_right:
        # State A: Empty State
        if not active_bytes and "last_pred" not in st.session_state:
            st.markdown("""
                <div class="kpi-card" style="text-align: center; padding: 60px 24px;">
                    <div style="font-size: 3rem; margin-bottom: 12px;">🧠</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">
                        No Scan Loaded Yet
                    </div>
                    <div style="font-size: 0.92rem; color: var(--text-secondary); max-width: 440px; margin: 0 auto; line-height: 1.5;">
                        Upload a cranial MRI image or click one of the pre-loaded verification samples on the left to begin AI-powered tumor localization.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # State B: Image loaded, awaiting analysis trigger
        elif active_bytes and not run_analysis and "last_pred" not in st.session_state:
            st.markdown("### Pre-Analysis Scan Preview")
            try:
                pil_img = Image.open(io.BytesIO(active_bytes))
                st.markdown(f"""
                    <div class="image-panel-card" style="margin-bottom: 14px;">
                        <div class="image-panel-header">
                            <span class="image-panel-title">Source: <code>{active_filename}</code></span>
                            <span class="image-panel-tag">{pil_img.size[0]} × {pil_img.size[1]} px • {pil_img.format or 'IMG'}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.image(pil_img, use_container_width=True)
            except Exception:
                st.error("Uploaded file could not be parsed as a valid image.")

        # State C: Run Analysis Triggered
        if run_analysis and active_bytes:
            # Scanning Animation Status
            with st.spinner("Analyzing cranial MRI scan with YOLOv8..."):
                st.markdown("""
                    <div class="scanning-box">
                        <div class="scanning-pulse-circle">🔬</div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: var(--text-primary);">
                            Analyzing Cranial MRI Scan...
                        </div>
                        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 6px;">
                            Running YOLOv8 deep feature pyramid inference &amp; bounding box localization
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                time.sleep(0.4)  # Subtle pacing for UI transition
                api_client = get_api_client()
                success, response_data = api_client.predict_image(
                    image_bytes=active_bytes,
                    filename=active_filename,
                    confidence=conf_threshold
                )

                if success:
                    st.session_state["last_pred"] = response_data
                    st.session_state["last_bytes"] = active_bytes
                    st.session_state["last_filename"] = active_filename

                    # Record to Session Scan History
                    if "scan_history" not in st.session_state:
                        st.session_state["scan_history"] = []
                    
                    st.session_state["scan_history"].insert(0, {
                        "id": f"scan_{int(time.time())}",
                        "filename": active_filename,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "count": response_data.get("count", 0),
                        "primary_class": response_data.get("detections", [{}])[0].get("class_name", "No Tumor") if response_data.get("count", 0) > 0 else "No Tumor",
                        "confidence": response_data.get("detections", [{}])[0].get("confidence", 0.0) if response_data.get("count", 0) > 0 else 0.0,
                        "pred": response_data,
                        "bytes": active_bytes
                    })
                    st.rerun()
                else:
                    st.error(f"Inference failed: {response_data.get('error', 'Unable to complete inference.')}")

        # State D: Results available
        if "last_pred" in st.session_state and active_bytes:
            render_result_panel(
                pred=st.session_state["last_pred"],
                orig_bytes=active_bytes,
                filename=st.session_state.get("last_filename", "scan.jpg")
            )

    render_disclaimer()
    render_footer()
