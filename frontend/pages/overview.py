import streamlit as st
import os
import io
import plotly.graph_objects as go
from PIL import Image

from frontend.components.cards import render_top_header, render_kpi_card, render_disclaimer, render_footer
from frontend.components.sample_selector import get_verified_samples
from frontend.services.api_client import get_api_client
from frontend.components.result_panel import base64_to_bytes

def render_overview_page(is_api_connected: bool):
    """
    Render enhanced, highly interactive Nuroscan Clinical Dashboard
    with live precision gauge, sandbox scan tester, and interactive class explorer.
    """
    render_top_header(
        title="Nuroscan Clinical Dashboard",
        description="High-precision computer vision platform for real-time brain MRI tumor localization & classification.",
        meta_text="System Status: Operational • Model: YOLOv8n (PyTorch) • Tensor: 640 × 640 RGB",
        badges=["YOLOv8n PyTorch", "FastAPI Microservice", "96.31% mAP@50", "Real-Time Inference"]
    )

    # --- 1. HERO BANNER ---
    st.markdown("""
        <div class="hero-banner-card">
            <div class="hero-title">Welcome to Nuroscan</div>
            <div class="hero-description">
                Nuroscan delivers automated bounding-box localization and classification of brain tumors 
                (Glioma, Meningioma, Pituitary) from cranial MRI scans. Explore the interactive sandbox below or launch the dedicated analysis suite.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Hero Action Buttons
    c_btn1, c_btn2, _ = st.columns([1.3, 1.4, 1.8])
    with c_btn1:
        if st.button("🔬 Open Full MRI Analyzer ➔", type="primary", use_container_width=True):
            st.session_state["current_page"] = "MRI Detection"
            st.rerun()
    with c_btn2:
        if st.button("📈 Explore Model Analytics ➔", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Model Analytics"
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- 2. INTERACTIVE ACCURACY GAUGE & KPIS ---
    st.markdown("### Empirical Performance Benchmarks")
    col_gauge, col_kpis = st.columns([1.1, 2], gap="large")

    with col_gauge:
        # Plotly Gauge Chart for mAP@50
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=96.31,
            number={'suffix': "%", 'font': {'size': 36, 'color': '#0284C7', 'family': 'Plus Jakarta Sans'}},
            title={'text': "<b>Validation mAP@50</b><br><span style='font-size:0.8em;color:#64748B'>Mean Average Precision</span>", 'font': {'size': 14, 'family': 'Plus Jakarta Sans'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
                'bar': {'color': "#0284C7", 'thickness': 0.28},
                'bgcolor': "#F1F5F9",
                'borderwidth': 1,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 60], 'color': 'rgba(239, 68, 68, 0.15)'},
                    {'range': [60, 85], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
                ],
                'threshold': {
                    'line': {'color': "#10B981", 'width': 3},
                    'thickness': 0.75,
                    'value': 96.31
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
            render_kpi_card("PRECISION", "93.87%", "Low False-Positive Rate", "🎯")
        with k2:
            render_kpi_card("RECALL", "94.01%", "High Tumor Sensitivity", "⚡")
        with k3:
            render_kpi_card("LATENCY", "~32 ms", "Real-Time Inference", "⏱️")

        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: var(--surface-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 14px 18px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                ⚡ <strong>YOLOv8 Single-Stage Backbone</strong> processes cranial MRI scans at 30+ frames per second, 
                performing dual feature extraction and bounding-box regression simultaneously.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # --- 3. INTERACTIVE LIVE SCAN SANDBOX ---
    st.markdown("### 🧪 Interactive Scan Sandbox")
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

            run_sandbox = st.button("⚡ Run Instant Detection", type="primary", use_container_width=True)

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
                            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-primary);">
                                🚨 {top_det['class_name']} Detected ({conf_pct:.1f}%)
                            </div>
                            <div style="font-size: 0.82rem; color: var(--text-secondary);">
                                Localized {count} lesion region(s) in {st.session_state.get('sandbox_name', 'MRI Scan')}.
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="result-banner-box result-banner-negative" style="padding: 16px; margin-bottom: 12px;">
                            <div style="font-size: 1.15rem; font-weight: 800; color: var(--text-primary);">
                                ✅ No Lesion Detected
                            </div>
                            <div style="font-size: 0.82rem; color: var(--text-secondary);">
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
                st.markdown("""
                    <div class="kpi-card" style="text-align: center; padding: 48px 20px;">
                        <div style="font-size: 2.5rem; margin-bottom: 8px;">🔬</div>
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
    st.markdown("### 🧠 Interactive Classification Reference")
    st.markdown("""
        <div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 14px;">
            Select a diagnosis class below to explore clinical pathology and diagnostic visual features.
        </div>
    """, unsafe_allow_html=True)

    tab_glioma, tab_mening, tab_pituit, tab_normal = st.tabs([
        "🔬 Glioma",
        "🛡️ Meningioma",
        "🎯 Pituitary",
        "✅ No Tumor (Normal)"
    ])

    with tab_glioma:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--text-primary);">Glioma (Class ID: 0)</div>
                    <span class="pill-status" style="background: rgba(239, 68, 68, 0.15); color: var(--danger);">High Clinical Priority</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    Gliomas originate from glial support cells in the brain and spinal cord. They are characteristically infiltrative, 
                    displaying heterogeneous signal intensity on T1/T2 MRI with marked peripheral ring contrast enhancement and surrounding vasogenic edema.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Anatomical Site:</strong> Cerebral Hemispheres</div>
                    <div><strong>Model Precision:</strong> 94.2%</div>
                    <div><strong>Key MRI Sequence:</strong> T1-Gadolinium / FLAIR</div>
                    <div><strong>Bounding Box Tag:</strong> Red Overlay</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with tab_mening:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--text-primary);">Meningioma (Class ID: 1)</div>
                    <span class="pill-status" style="background: rgba(245, 158, 11, 0.15); color: var(--warning);">Extra-Axial Neoplasm</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    Arising from the arachnoid cap cells of the meninges, meningiomas are typically extra-axial, well-circumscribed, and benign. 
                    They exhibit intense, homogeneous enhancement and frequently display a characteristic 'dural tail' sign on post-contrast imaging.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Anatomical Site:</strong> Dural Surfaces / Skull Base</div>
                    <div><strong>Model Precision:</strong> 93.5%</div>
                    <div><strong>Key MRI Sequence:</strong> Post-Contrast T1w</div>
                    <div><strong>Bounding Box Tag:</strong> Cyan Overlay</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with tab_pituit:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--text-primary);">Pituitary Adenoma (Class ID: 3)</div>
                    <span class="pill-status" style="background: rgba(14, 165, 233, 0.15); color: var(--info);">Sellar Region</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    Neoplasms localized within the sella turcica originating from anterior pituitary cells. They can expand superiorly to cause optic chiasm compression, 
                    visible as discrete focal lesions with delayed contrast wash-in compared to normal pituitary parenchyma.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Anatomical Site:</strong> Sella Turcica / Skull Base</div>
                    <div><strong>Model Precision:</strong> 95.1%</div>
                    <div><strong>Key MRI Sequence:</strong> Dynamic Coronal T1w</div>
                    <div><strong>Bounding Box Tag:</strong> Purple Overlay</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with tab_normal:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.2rem; font-weight: 800; color: var(--text-primary);">No Tumor / Healthy Scan (Class ID: 2)</div>
                    <span class="pill-status pill-online">Normal Anatomy</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                    Healthy cranial MRI displaying symmetric cerebral hemispheres, distinct grey-white matter differentiation, normal ventricular architecture, 
                    and absence of focal mass effect, abnormal contrast enhancement, or midline shift.
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 0.84rem;">
                    <div><strong>Anatomical Site:</strong> Symmetric Parenchyma</div>
                    <div><strong>Model Specificity:</strong> 97.4%</div>
                    <div><strong>Key MRI Sequence:</strong> T1, T2, FLAIR</div>
                    <div><strong>Result Status:</strong> Zero Bounding Boxes</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    render_disclaimer()
    render_footer()
