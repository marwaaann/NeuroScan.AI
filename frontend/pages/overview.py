import streamlit as st
from frontend.components.cards import render_top_header, render_stat_card, render_disclaimer, render_footer

def render_overview_page(is_api_connected: bool):
    render_top_header(
        title="Overview",
        description="Brain MRI analysis powered by YOLOv8 computer vision.",
        meta_text=f"API Status: {'Connected' if is_api_connected else 'Offline'} • Engine: PyTorch • Resolution: 640 × 640"
    )

    # Hero Card
    st.markdown("""
        <div class="ns-surface-card" style="padding: 32px;">
            <div style="font-size: 1.6rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">
                Brain MRI Analysis
            </div>
            <div style="color: var(--text-secondary); font-size: 1rem; max-width: 750px; margin-bottom: 20px; line-height: 1.5;">
                Detect and localize brain tumor regions from MRI scans using computer vision.
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Analyze MRI ➔", type="primary"):
        st.session_state["current_page"] = "Detection"
        st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Compact Statistics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_stat_card("MODEL", "YOLOv8n", "Ultralytics Engine")
    with c2:
        render_stat_card("CLASSES", "4", "Glioma, Meningioma, Pituitary, Normal")
    with c3:
        render_stat_card("INPUT", "640 × 640", "RGB Tensor Matrix")
    with c4:
        render_stat_card("TASK", "Object Detection", "Bounding Box Localization")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Analysis Workspace Section
    st.markdown("### Your Analysis Workspace")
    st.markdown("""
        <div class="ns-surface-card" style="text-align: center; padding: 36px;">
            <div style="font-size: 1.05rem; font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">
                Ready for Analysis
            </div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                Upload an MRI scan to begin an analysis.
            </div>
        </div>
    """, unsafe_allow_html=True)

    render_disclaimer()
    render_footer()
