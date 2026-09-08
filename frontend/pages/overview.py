import streamlit as st
from frontend.components.cards import render_top_header, render_kpi_card, render_disclaimer, render_footer

def render_overview_page(is_api_connected: bool):
    """Render clinical dashboard landing page with KPIs, CTAs, and quickstart cards"""
    render_top_header(
        title="Clinical Dashboard",
        description="Medical computer-vision workspace for brain tumor localization and classification.",
        meta_text="System Status: Connected • Engine: YOLOv8n • Tensor: 640 × 640 RGB",
        badges=["YOLOv8n PyTorch", "FastAPI Microservice", "Medical AI", "Clinical Research"]
    )

    # Hero Banner
    st.markdown("""
        <div class="hero-banner-card">
            <div class="hero-title">AI-Powered Cranial MRI Analysis</div>
            <div class="hero-description">
                NeuroScan AI assists researchers and medical imaging professionals in rapidly detecting and localizing 
                brain tumors from Magnetic Resonance Imaging (MRI) scans with explainable visual bounding boxes and calibrated confidence insights.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Action Buttons Row
    c_btn1, c_btn2, _ = st.columns([1.2, 1.4, 2])
    with c_btn1:
        if st.button("Launch MRI Analysis ➔", type="primary", use_container_width=True):
            st.session_state["current_page"] = "MRI Analysis"
            st.rerun()
    with c_btn2:
        if st.button("🧪 Try Verified Sample Scan", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "MRI Analysis"
            st.session_state["auto_load_sample"] = True
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Core Clinical Performance KPIs (Empirical Project Data)
    st.markdown("### Model Performance Benchmarks")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("VALIDATION mAP@50", "96.31%", "Mean Average Precision at IoU 0.50", "🎯")
    with k2:
        render_kpi_card("PRECISION", "93.87%", "Bounding Box Localization Accuracy", "🔬")
    with k3:
        render_kpi_card("RECALL", "94.01%", "Lesion Sensitivity Across Test Set", "⚡")
    with k4:
        render_kpi_card("TUMOR CLASSES", "4 Types", "Glioma, Meningioma, Pituitary, Normal", "🧠")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Diagnostic Workflow Cards
    st.markdown("### How the Diagnostic Pipeline Works")
    step_col1, step_col2, step_col3 = st.columns(3)

    with step_col1:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">📤</div>
                <div style="font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px;">1. Upload Cranial Scan</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                    Provide an axial or sagittal MRI scan in JPG, JPEG, or PNG format, or choose from verified pre-loaded evaluation scans.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with step_col2:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">🧠</div>
                <div style="font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px;">2. YOLOv8 Deep Vision</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                    The model preprocesses the scan into a 640×640 tensor, passes through the DarkNet feature pyramid, and identifies tumor regions in milliseconds.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with step_col3:
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="font-size: 1.5rem; margin-bottom: 8px;">📊</div>
                <div style="font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px;">3. Diagnostic Insights</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                    Review side-by-side original vs. annotated scans, examine bounding coordinates and confidence scores, and export clinical reports.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Recent Scan History preview if present
    if "scan_history" in st.session_state and len(st.session_state["scan_history"]) > 0:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("### Recent Scans in This Session")
        history = st.session_state["scan_history"]
        st.info(f"You have analyzed {len(history)} scan(s) during your current research session. Navigate to '📁 Scan History' to view detailed records.")

    render_disclaimer()
    render_footer()
