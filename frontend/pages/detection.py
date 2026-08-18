import streamlit as st
import io
import base64
import os
import json
import pandas as pd
from PIL import Image

from frontend.components.cards import render_top_header, render_stat_card, render_disclaimer, render_footer
from frontend.services.api_client import get_api_client

def base64_to_bytes(base64_str: str) -> bytes:
    """Decode base64 string into PNG bytes"""
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    return base64.b64decode(base64_str)

def get_sample_scans():
    """Locate sample MRI files in workspace dataset"""
    samples = [
        ("Glioma Sample", os.path.join("brain_tumor_dataset", "Train", "images", "gg (105).jpg")),
        ("Validation Scan #1", os.path.join("brain_tumor_dataset", "Val", "images", "gg (10).jpg")),
        ("Validation Scan #2", os.path.join("brain_tumor_dataset", "Val", "images", "gg (131).jpg"))
    ]
    return [(label, p) for label, p in samples if os.path.exists(p)]

def render_detection_page(is_api_connected: bool):
    render_top_header(
        title="Brain MRI Detection",
        description="Analyze an MRI image using the YOLOv8 detection model.",
        meta_text="Model: YOLOv8n • API: Connected" if is_api_connected else "Model: YOLOv8n • API: Offline"
    )

    if not is_api_connected:
        st.error("""
            **Backend unavailable**  
            We couldn't connect to the FastAPI inference service. Make sure the backend is running on `localhost:8000`.
        """)

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.markdown("### Upload MRI Scan")
        
        uploaded_file = st.file_uploader(
            "Drop MRI image here or click to browse",
            type=["png", "jpg", "jpeg"],
            help="Supported formats: PNG, JPG, JPEG"
        )

        samples = get_sample_scans()
        selected_sample_path = None
        
        if samples:
            st.markdown("**Use sample scan:**")
            demo_choice = st.selectbox("Sample scans dropdown", ["-- Select a sample scan --"] + [label for label, _ in samples], label_visibility="collapsed")
            if demo_choice != "-- Select a sample scan --":
                for label, path in samples:
                    if label == demo_choice:
                        selected_sample_path = path
                        break

        st.markdown("### Inference Settings")
        conf_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.10,
            max_value=0.95,
            value=0.50,
            step=0.05
        )
        st.markdown("<div style='font-size: 0.8rem; color: var(--text-secondary); margin-top: -10px; margin-bottom: 16px;'>Model: YOLOv8n</div>", unsafe_allow_html=True)

        can_run = (uploaded_file is not None) or (selected_sample_path is not None)
        run_btn = st.button("Run Analysis", type="primary", disabled=not can_run, use_container_width=True)

    with col_right:
        image_bytes = None
        filename = ""
        file_format = ""
        img_size = (0, 0)

        if uploaded_file is not None:
            image_bytes = uploaded_file.getvalue()
            filename = uploaded_file.name
            file_format = uploaded_file.type.split("/")[-1].upper()
            try:
                pil_temp = Image.open(io.BytesIO(image_bytes))
                img_size = pil_temp.size
            except Exception:
                pass
        elif selected_sample_path is not None:
            with open(selected_sample_path, "rb") as f:
                image_bytes = f.read()
            filename = os.path.basename(selected_sample_path)
            file_format = filename.split(".")[-1].upper()
            try:
                pil_temp = Image.open(io.BytesIO(image_bytes))
                img_size = pil_temp.size
            except Exception:
                pass

        if image_bytes and not run_btn and 'last_pred' not in st.session_state:
            st.markdown("### Scan Preview")
            st.markdown(f"**File name**: `{filename}` &nbsp;|&nbsp; **Dimensions**: `{img_size[0]} × {img_size[1]} px` &nbsp;|&nbsp; **Format**: `{file_format}`")
            st.image(Image.open(io.BytesIO(image_bytes)), use_container_width=True)

        if run_btn and image_bytes:
            with st.spinner("Analyzing MRI...\n• Loading model...\n• Processing image...\n• Running YOLOv8 inference...\n• Preparing results..."):
                api_client = get_api_client()
                success, response_data = api_client.predict_image(
                    image_bytes=image_bytes,
                    filename=filename,
                    confidence=conf_threshold
                )
                if success:
                    st.session_state['last_pred'] = response_data
                    st.session_state['last_filename'] = filename
                    st.session_state['last_bytes'] = image_bytes
                else:
                    st.error(f"Analysis failed: {response_data.get('error', 'Please try another scan.')}")

        # Render Results
        if 'last_pred' in st.session_state:
            pred = st.session_state['last_pred']
            count = pred.get("count", 0)
            detections = pred.get("detections", [])

            st.markdown("## Analysis Complete")

            # Equal Image Panels
            c_orig, c_det = st.columns(2)
            with c_orig:
                st.markdown("#### Original Scan")
                orig_b = st.session_state['last_bytes']
                st.image(Image.open(io.BytesIO(orig_b)), use_container_width=True)

            with c_det:
                st.markdown("#### Detection Result")
                if pred.get("annotated_image"):
                    ann_bytes = base64_to_bytes(pred["annotated_image"])
                    st.image(Image.open(io.BytesIO(ann_bytes)), use_container_width=True)

                    st.download_button(
                        label="Download Annotated Image",
                        data=ann_bytes,
                        file_name=f"annotated_{st.session_state.get('last_filename', 'mri.png')}",
                        mime="image/png",
                        type="secondary",
                        use_container_width=True
                    )

            st.markdown("---")

            # Detection Summary & No-Detection Empty State
            if count > 0:
                st.markdown("### Detection Summary")
                m1, m2, m3 = st.columns(3)
                with m1:
                    render_stat_card("Primary Detection", detections[0]['class_name'])
                with m2:
                    render_stat_card("Confidence", f"{detections[0]['confidence']*100:.2f}%")
                with m3:
                    render_stat_card("Total Detections", str(count))

                st.markdown("<br/>", unsafe_allow_html=True)
                st.markdown("### Detection Details")
                
                rows = []
                for idx, d in enumerate(detections, 1):
                    bbox = d['bbox']
                    rows.append({
                        "#": idx,
                        "Class": d['class_name'],
                        "Confidence": f"{d['confidence']*100:.2f}%",
                        "X1": round(bbox['x1'], 2),
                        "Y1": round(bbox['y1'], 2),
                        "X2": round(bbox['x2'], 2),
                        "Y2": round(bbox['y2'], 2)
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

                with st.expander("Raw Detection Payload (JSON)"):
                    st.code(json.dumps(pred, indent=2), language="json")
            else:
                st.markdown("""
                    <div class="ns-surface-card" style="border-left: 4px solid var(--warning-color); padding: 20px;">
                        <div style="font-weight: 700; font-size: 1.05rem; color: var(--text-primary); margin-bottom: 4px;">
                            No detections found
                        </div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">
                            The model did not produce a detection above the selected confidence threshold.<br/>
                            Try adjusting the threshold or analyzing another image.
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    render_disclaimer()
    render_footer()
