import streamlit as st
from frontend.components.cards import render_top_header, render_disclaimer, render_footer
from frontend.components.contact_form import render_contact_form

def render_contact_page():
    """
    Renders the dedicated Contact & Consultation page inspired by NURA health screening centers.
    """
    render_top_header(
        title="Clinical Consultation & Inquiry",
        description="Connect with the Nuroscan team for AI screening demonstrations, clinical research collaborations, or hospital pilot programs.",
        meta_text="Official Inquiry Portal • IIIT Sonepat Research Initiative • Response Time: Within 24h",
        badges=["AI Screening", "Clinical Collaboration", "IIIT Sonepat Research", "PACS Integration"]
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="kpi-card" style="padding: 20px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">🏥</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: var(--navy-header); margin-bottom: 4px;">
                    Clinical Screening
                </div>
                <div style="font-size: 0.84rem; color: var(--text-secondary); line-height: 1.5;">
                    Deploy Nuroscan's automated YOLOv8 inference as a second-reader assistant in diagnostic imaging workflows.
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="kpi-card" style="padding: 20px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">🔬</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: var(--navy-header); margin-bottom: 4px;">
                    Academic Research
                </div>
                <div style="font-size: 0.84rem; color: var(--text-secondary); line-height: 1.5;">
                    Access paper benchmarks, dataset annotations (7,000+ MRI scans), and YOLOv8/YOLOv11 comparative weights.
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="kpi-card" style="padding: 20px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">⚡</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: var(--navy-header); margin-bottom: 4px;">
                    API &amp; Integration
                </div>
                <div style="font-size: 0.84rem; color: var(--text-secondary); line-height: 1.5;">
                    Integrate high-throughput REST endpoints into existing hospital PACS / RIS / DICOM viewers.
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Render the NURA Form
    render_contact_form()

    render_disclaimer()
    render_footer()
