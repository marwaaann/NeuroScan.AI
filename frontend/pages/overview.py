import streamlit as st
import os
import io
import plotly.graph_objects as go
from PIL import Image

from frontend.components.cards import render_top_header, render_kpi_card, render_disclaimer, render_footer
from frontend.components.sample_selector import get_verified_samples
from frontend.services.api_client import get_api_client
from frontend.components.result_panel import base64_to_bytes
from frontend.components.contact_form import render_contact_form
from frontend.components.icons import get_svg_icon

def render_overview_page(is_api_connected: bool):
    """
    Render NURA-inspired NeuroScan.AI Brain Health Screening Dashboard
    with live precision gauge, sandbox scan tester, research paper metrics,
    and embedded consultation form.
    """
    render_top_header(
        title="NeuroScan.AI — AI Brain Health Screening Platform",
        description="Automated cranial MRI brain tumor localization and multi-class screening powered by YOLO deep learning architectures.",
        meta_text="Empirical Research: IIIT Sonepat (Rishabh, Marwan et al.) • 7,500+ Scans • 92 FPS Real-Time Inference",
        badges=["NURA Clinical Screening", "IIIT Sonepat Research", "95% System Accuracy", "Multi-Planar MRI (Axial, Sagittal, Coronal)"]
    )

    # --- 1. HERO BANNER (NURA HEALTHCARE AESTHETIC) ---
    st.markdown("""
        <div class="hero-banner-card">
            <div class="hero-title">Precision AI Brain Health Screening</div>
            <div class="hero-description">
                Inspired by modern preventative AI screening centers, NeuroScan.AI combines state-of-the-art 
                single-stage deep learning (YOLOv8 &amp; YOLOv11) with multi-planar cranial MRI analysis to deliver 
                instantaneous lesion localization and multi-class classification in under 35 milliseconds.
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 8px;">
                <span class="tech-badge" style="background: rgba(0, 168, 150, 0.12); color: #007E70; border-color: rgba(0, 168, 150, 0.3);">92 FPS Real-Time Speed</span>
                <span class="tech-badge" style="background: rgba(2, 132, 199, 0.12); color: #0284C7; border-color: rgba(2, 132, 199, 0.3);">7,500+ MRI Training Cohort</span>
                <span class="tech-badge" style="background: rgba(16, 185, 129, 0.12); color: #059669; border-color: rgba(16, 185, 129, 0.3);">95% System Accuracy</span>
                <span class="tech-badge" style="background: rgba(99, 102, 241, 0.12); color: #4F46E5; border-color: rgba(99, 102, 241, 0.3);">3 Planes (Axial, Sagittal, Coronal)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Hero Action Buttons
    c_btn1, c_btn2, c_btn3 = st.columns([1.3, 1.3, 1.4])
    with c_btn1:
        if st.button("Open Full MRI Analyzer ➔", type="primary", use_container_width=True):
            st.session_state["current_page"] = "MRI Detection"
            st.rerun()
    with c_btn2:
        if st.button("Explore Model Analytics ➔", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Model Analytics"
            st.rerun()
    with c_btn3:
        if st.button("Request Consultation ➔", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Contact Us"
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- 2. INTERACTIVE ACCURACY GAUGE & KPIS ---
    st.markdown("### Empirical Performance Benchmarks (IIIT Sonepat Research)")
    col_gauge, col_kpis = st.columns([1.1, 2], gap="large")

    with col_gauge:
        # Plotly Gauge Chart for Overall Accuracy (95%)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=95.0,
            number={'suffix': "%", 'font': {'size': 38, 'color': '#00A896', 'family': 'Plus Jakarta Sans'}},
            title={'text': "<b>Overall System Accuracy</b><br><span style='font-size:0.8em;color:#627D98'>Empirical Validation (7,500+ Scans)</span>", 'font': {'size': 14, 'family': 'Plus Jakarta Sans'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
                'bar': {'color': "#00A896", 'thickness': 0.28},
                'bgcolor': "#F1F7F6",
                'borderwidth': 1,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 60], 'color': 'rgba(239, 68, 68, 0.15)'},
                    {'range': [60, 85], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [85, 100], 'color': 'rgba(0, 168, 150, 0.15)'}
                ],
                'threshold': {
                    'line': {'color': "#008C7D", 'width': 3},
                    'thickness': 0.75,
                    'value': 95.0
                }
            }
        ))
        fig_gauge.update_layout(
            height=240,
            margin=dict(l=15, r=15, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_kpis:
        st.markdown("<div style='height: 14px'></div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1:
            render_kpi_card("PRECISION", "96.0%", "Low False-Positive Rate", "precision")
        with k2:
            render_kpi_card("RECALL (SENSITIVITY)", "94.0%", "High Lesion Catch Rate", "sensitivity")
        with k3:
            render_kpi_card("INFERENCE RATE", "92 FPS", "~32 ms per cranial slice", "speed")

        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: var(--surface-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 14px 18px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                ⚡ <strong>Multi-Planar Dataset Cohort:</strong> Model evaluated on 7,000–8,000 axial, sagittal, and coronal MRI scans 
                resized to 640×640. YOLO architecture executes single-pass bounding box regression and multi-class classification simultaneously.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- 3. INTERACTIVE LIVE SCAN SANDBOX ---
    st.markdown("### Interactive Scan Sandbox")
    st.markdown("""
        <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 16px;">
            Test the YOLOv8 model immediately right here on the dashboard without uploading files.
        </div>
    """, unsafe_allow_html=True)

    samples = get_verified_samples()
    if samples:
        sandbox_col_left, sandbox_col_right = st.columns([1, 1.4], gap="large")

        with sandbox_col_left:
            st.markdown("#### 1. Select a Verified Sample Scan")
            sample_names = [s["name"] for s in samples]
            selected_name = st.radio("Choose scan", sample_names, index=0, label_visibility="collapsed")
            
            selected_item = next(s for s in samples if s["name"] == selected_name)
            
            # Show thumbnail
            try:
                thumb = Image.open(selected_item["path"])
                st.image(thumb, caption=f"{selected_item['name']} ({selected_item['type_badge']})", use_container_width=True)
            except Exception:
                pass

            st.markdown(f"<div style='font-size: 0.82rem; color: var(--text-muted); margin-bottom: 12px;'>{selected_item['description']}</div>", unsafe_allow_html=True)

            sandbox_conf = st.slider(
                "Confidence Threshold",
                min_value=0.10,
                max_value=0.90,
                value=0.45,
                step=0.05,
                key="sandbox_conf"
            )

            run_sandbox = st.button("Run Instant Detection ➔", type="primary", use_container_width=True)

        with sandbox_col_right:
            st.markdown("#### 2. AI Localization Output")
            
            if run_sandbox:
                with st.spinner("Processing MRI scan..."):
                    with open(selected_item["path"], "rb") as f:
                        sb_bytes = f.read()
                    
                    api_client = get_api_client()
                    success, result = api_client.predict_image(
                        image_bytes=sb_bytes,
                        filename=os.path.basename(selected_item["path"]),
                        confidence=sandbox_conf
                    )

                    if success:
                        st.session_state["sandbox_result"] = result
                        st.session_state["sandbox_bytes"] = sb_bytes
                        st.session_state["sandbox_name"] = selected_item["name"]
                    else:
                        st.error(f"Inference error: {result.get('error')}")

            if "sandbox_result" in st.session_state:
                res = st.session_state["sandbox_result"]
                count = res.get("count", 0)
                detections = res.get("detections", [])

                if count > 0:
                    top_det = detections[0]
                    conf_pct = top_det["confidence"] * 100
                    st.markdown(f"""
                        <div class="result-banner-box result-banner-positive" style="padding: 16px; margin-bottom: 12px;">
                            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                                {get_svg_icon('alert', size=22, color='#DC2626')} {top_det['class_name']} Detected ({conf_pct:.1f}%)
                            </div>
                            <div style="font-size: 0.82rem; color: var(--text-secondary); margin-top: 4px;">
                                Localized {count} lesion region(s) in {st.session_state.get('sandbox_name', 'MRI Scan')}.
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="result-banner-box result-banner-negative" style="padding: 16px; margin-bottom: 12px;">
                            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                                {get_svg_icon('check', size=22, color='#059669')} No Lesion Detected
                            </div>
                            <div style="font-size: 0.82rem; color: var(--text-secondary); margin-top: 4px;">
                                Tissue appears healthy above current confidence threshold.
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                if res.get("annotated_image"):
                    ann_img = Image.open(io.BytesIO(base64_to_bytes(res["annotated_image"])))
                    st.image(ann_img, caption="YOLOv8 Detection Overlay with Bounding Box", use_container_width=True)

                if st.button("Open Full MRI Analyzer with This Scan ➔", type="secondary", use_container_width=True):
                    st.session_state["last_pred"] = res
                    st.session_state["last_bytes"] = st.session_state["sandbox_bytes"]
                    st.session_state["last_filename"] = os.path.basename(selected_item["path"])
                    st.session_state["current_page"] = "MRI Detection"
                    st.rerun()
            else:
                st.markdown(f"""
                    <div class="kpi-card" style="text-align: center; padding: 48px 20px;">
                        <div style="margin-bottom: 12px;">{get_svg_icon('scan', size=42, color='var(--primary)')}</div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px;">
                            Sandbox Awaiting Execution
                        </div>
                        <div style="font-size: 0.85rem; color: var(--text-secondary); max-width: 320px; margin: 0 auto;">
                            Click <strong>'Run Instant Detection'</strong> on the left to see YOLOv8 bounding boxes in real time.
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- 4. INTERACTIVE TUMOR CLASS EXPLORER ---
    st.markdown("### Pathology Classification Reference")
    st.markdown("""
        <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 14px;">
            Select a diagnostic class below to explore clinical pathology, visual biomarkers, and model accuracy.
        </div>
    """, unsafe_allow_html=True)

    tab_glioma, tab_mening, tab_pituit, tab_normal = st.tabs([
        "Glioma (Class 0)",
        "Meningioma (Class 1)",
        "Pituitary Adenoma (Class 3)",
        "Healthy Tissue (Class 2)"
    ])

    with tab_glioma:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--navy-header);">Glioma (Class ID: 0)</div>
                    <span class="pill-status" style="background: rgba(239, 68, 68, 0.15); color: var(--danger);">High Clinical Priority • 90% Accuracy</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    From IIIT Sonepat Study: Irregularly shaped, with indistinct borders, highly malignant tumors originating from glial cells, 
                    diffusely located across cerebral parenchyma. Infiltrative patterns exhibit heterogeneous intensity on T1/T2 MRI with surrounding edema.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Dataset Scans:</strong> ~2,200 Scans (28%)</div>
                    <div><strong>Model Accuracy:</strong> 90.0%</div>
                    <div><strong>Key MRI Sequence:</strong> T1-Gadolinium / FLAIR</div>
                    <div><strong>Bounding Box Tag:</strong> Red Overlay (Class 0)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with tab_mening:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--navy-header);">Meningioma (Class ID: 1)</div>
                    <span class="pill-status" style="background: rgba(16, 185, 129, 0.15); color: #059669;">Extra-Axial • 99% Accuracy</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    From IIIT Sonepat Study: Typically benign, well-defined, and localized neoplasms arising from arachnoid cap cells of the meninges. 
                    They exhibit distinct margins, homogeneous contrast enhancement, and a characteristic dural tail sign.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Dataset Scans:</strong> ~1,900 Scans (25%)</div>
                    <div><strong>Model Accuracy:</strong> 99.0%</div>
                    <div><strong>Key MRI Sequence:</strong> Contrast-Enhanced T1w</div>
                    <div><strong>Bounding Box Tag:</strong> Cyan Overlay (Class 1)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with tab_pituit:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--navy-header);">Pituitary Adenoma (Class ID: 3)</div>
                    <span class="pill-status" style="background: rgba(14, 165, 233, 0.15); color: var(--info);">Sellar Region • 94% Accuracy</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    From IIIT Sonepat Study: Neoplasms localized within the sella turcica originating from anterior pituitary cells. 
                    May expand superiorly into the suprasellar cistern with optic chiasm compression, showing focal signal asymmetry on coronal scans.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Dataset Scans:</strong> ~1,600 Scans (21%)</div>
                    <div><strong>Model Accuracy:</strong> 94.0%</div>
                    <div><strong>Key MRI Sequence:</strong> Coronal T1w High-Res</div>
                    <div><strong>Bounding Box Tag:</strong> Purple Overlay (Class 3)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with tab_normal:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--navy-header);">No Tumor / Healthy Scan (Class ID: 2)</div>
                    <span class="pill-status pill-online">Normal Tissue • 100% Accuracy</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    From IIIT Sonepat Study: Healthy cranial MRI displaying symmetric hemispheres, normal sulcal pattern, distinct grey-white matter interface, 
                    and absence of mass effect or pathological enhancement. Achieved perfect specificity with zero false alarms.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Dataset Scans:</strong> ~1,300–1,500 Scans</div>
                    <div><strong>Model Accuracy:</strong> 100.0% (Zero False Alarms)</div>
                    <div><strong>Key MRI Sequence:</strong> Multi-Planar T1/T2/FLAIR</div>
                    <div><strong>Result Status:</strong> Zero Bounding Boxes</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- 5. NURA-INSPIRED CONSULTATION & CONTACT SECTION ---
    render_contact_form()

    render_disclaimer()
    render_footer()
