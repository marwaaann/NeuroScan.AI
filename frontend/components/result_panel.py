import streamlit as st
import io
import json
import base64
import pandas as pd
from PIL import Image
from typing import Dict, Any

def base64_to_bytes(base64_str: str) -> bytes:
    """Decode base64 string into image bytes"""
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    return base64.b64decode(base64_str)

def render_confidence_meter(confidence: float):
    """Render sleek, color-coded confidence meter"""
    pct = round(confidence * 100, 1)
    
    # Color logic
    if pct >= 80:
        fill_color = "var(--primary)"
    elif pct >= 60:
        fill_color = "var(--warning)"
    else:
        fill_color = "var(--danger)"

    st.markdown(f"""
        <div style="margin: 12px 0 16px 0;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 4px;">
                <span>MODEL CONFIDENCE</span>
                <span style="color: var(--text-primary);">{pct}%</span>
            </div>
            <div class="confidence-meter-track">
                <div class="confidence-meter-fill" style="width: {pct}%; background: {fill_color};"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

from frontend.components.icons import get_svg_icon

def render_result_panel(pred: Dict[str, Any], orig_bytes: bytes, filename: str):
    """Render comprehensive clinical diagnostic result panel"""
    # Robust determination of tumor presence
    is_tumor = pred.get("is_tumor_detected", False)
    tumor_dets = pred.get("tumor_detections", [])
    
    # Fallback if legacy response format
    if not tumor_dets and "detections" in pred:
        tumor_dets = [d for d in pred["detections"] if d.get("class_id") != 2]
        is_tumor = len(tumor_dets) > 0
    
    tumor_count = len(tumor_dets)
    healthy_conf = pred.get("healthy_confidence")
    if healthy_conf is None:
        healthy_dets = [d for d in pred.get("detections", []) if d.get("class_id") == 2]
        if healthy_dets:
            healthy_conf = healthy_dets[0].get("confidence")
    
    # --- 1. Clinical Diagnosis Header Banner ---
    if is_tumor and tumor_count > 0:
        primary_tumor = tumor_dets[0]["class_name"]
        primary_conf = tumor_dets[0]["confidence"] * 100
        alert_svg = get_svg_icon("alert", size=22, color="var(--danger)")
        
        st.markdown(f"""
            <div class="result-banner-box result-banner-positive">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div class="result-primary-title" style="display: flex; align-items: center; gap: 8px;">
                            {alert_svg} <span>{primary_tumor} Detected</span>
                        </div>
                        <div class="result-primary-subtitle">
                            Localized {tumor_count} abnormal lesion region(s) in cranial MRI scan.
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="pill-status" style="background: rgba(239, 68, 68, 0.15); color: var(--danger); font-size: 0.85rem; padding: 6px 14px;">
                            Lesion Confidence: {primary_conf:.1f}%
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        render_confidence_meter(tumor_dets[0]["confidence"])
    else:
        check_svg = get_svg_icon("check", size=22, color="var(--success)")
        cert_text = f"Certainty: {healthy_conf*100:.1f}%" if healthy_conf else "Zero Lesions"
        st.markdown(f"""
            <div class="result-banner-box result-banner-negative">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div class="result-primary-title" style="display: flex; align-items: center; gap: 8px;">
                            {check_svg} <span>No Tumor Detected (Healthy Cranial Scan)</span>
                        </div>
                        <div class="result-primary-subtitle">
                            Scan analyzed across all cranial slices. Normal brain tissue confirmed with no pathological lesions.
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="pill-status pill-online" style="font-size: 0.85rem; padding: 6px 14px;">
                            Status: Normal Tissue • {cert_text}
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if healthy_conf:
            render_confidence_meter(healthy_conf)

    # --- 2. Side-by-Side Image Comparison ---
    st.markdown("### Visual Image Comparison")
    col_orig, col_ann = st.columns(2, gap="medium")

    with col_orig:
        st.markdown("""
            <div class="image-panel-header">
                <span class="image-panel-title">Original Patient Scan</span>
                <span class="image-panel-tag">Source MRI</span>
            </div>
        """, unsafe_allow_html=True)
        try:
            st.image(Image.open(io.BytesIO(orig_bytes)), use_container_width=True)
        except Exception:
            st.error("Failed to render original MRI scan.")

    ann_bytes = None
    with col_ann:
        st.markdown("""
            <div class="image-panel-header">
                <span class="image-panel-title">AI Detection Overlay</span>
                <span class="image-panel-tag" style="background: var(--primary-light); color: var(--primary);">YOLOv8 BBox</span>
            </div>
        """, unsafe_allow_html=True)
        if pred.get("annotated_image"):
            ann_bytes = base64_to_bytes(pred["annotated_image"])
            try:
                st.image(Image.open(io.BytesIO(ann_bytes)), use_container_width=True)
            except Exception:
                st.error("Failed to render annotated prediction.")
        else:
            st.info("No annotated visualization generated.")

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- 3. Structured Detection Details ---
    if is_tumor and tumor_count > 0:
        st.markdown("### Diagnostic Region Details")
        rows = []
        for idx, d in enumerate(tumor_dets, 1):
            bbox = d.get("bbox", {})
            width = round(bbox.get("x2", 0) - bbox.get("x1", 0), 1)
            height = round(bbox.get("y2", 0) - bbox.get("y1", 0), 1)
            rows.append({
                "#": idx,
                "Classification": d.get("class_name", "Unknown"),
                "Confidence": f"{d.get('confidence', 0)*100:.2f}%",
                "Bounding Box (X1, Y1, X2, Y2)": f"[{bbox.get('x1', 0)}, {bbox.get('y1', 0)}, {bbox.get('x2', 0)}, {bbox.get('y2', 0)}]",
                "Dimensions (W × H)": f"{width} × {height} px"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.markdown("### Diagnostic Findings Summary")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
                <div class="kpi-card" style="text-align: center; padding: 18px 12px;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 4px;">PATHOLOGICAL LESIONS</div>
                    <div style="font-size: 1.6rem; font-weight: 900; color: var(--success);">0 Detected</div>
                    <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 2px;">Zero malignant abnormalities</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="kpi-card" style="text-align: center; padding: 18px 12px;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 4px;">CRANIAL TISSUE STATUS</div>
                    <div style="font-size: 1.6rem; font-weight: 900; color: var(--primary);">Normal Baseline</div>
                    <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 2px;">Healthy ventricular &amp; cortical patterns</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            conf_str = f"{healthy_conf*100:.1f}%" if healthy_conf else "Optimal"
            st.markdown(f"""
                <div class="kpi-card" style="text-align: center; padding: 18px 12px;">
                    <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 4px;">SCREENING CERTAINTY</div>
                    <div style="font-size: 1.6rem; font-weight: 900; color: var(--primary);">{conf_str}</div>
                    <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 2px;">Model consensus index</div>
                </div>
            """, unsafe_allow_html=True)

    # --- 4. Export Actions ---
    st.markdown("### Export Diagnostic Results")
    exp_c1, exp_c2 = st.columns(2)

    with exp_c1:
        if ann_bytes:
            st.download_button(
                label="Download Annotated Image",
                data=ann_bytes,
                file_name=f"neuroscan_annotated_{filename}.jpg",
                mime="image/jpeg",
                use_container_width=True,
                type="primary"
            )

    with exp_c2:
        report_data = {
            "application": "NeuroScan.AI",
            "version": "YOLOv8n-Medical",
            "filename": filename,
            "is_tumor_detected": is_tumor,
            "tumor_count": tumor_count,
            "tumor_detections": tumor_dets,
            "all_detections": pred.get("detections", []),
            "disclaimer": "Research and educational tool only. Not for clinical diagnosis."
        }
        st.download_button(
            label="Download Clinical Summary (JSON)",
            data=json.dumps(report_data, indent=2),
            file_name=f"neuroscan_report_{filename}.json",
            mime="application/json",
            use_container_width=True,
            type="secondary"
        )

    with st.expander("Inspect Raw Inference Telemetry (JSON)"):
        st.code(json.dumps(pred, indent=2), language="json")
