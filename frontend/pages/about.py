import streamlit as st
from frontend.components.cards import render_top_header, render_disclaimer, render_footer

def render_about_page():
    """Render About NeuroScan page with technology stack, project mission, and author attribution"""
    render_top_header(
        title="About Nuroscan",
        description="An open-source medical imaging AI initiative applying computer vision to brain tumor detection.",
        meta_text="Version: 2.2 • Author: Marwan Shafi • License: Research & Education",
        badges=["Open Source", "Medical Vision", "Deep Learning", "Portfolio Project"]
    )

    col1, col2 = st.columns([1.6, 1.2], gap="large")

    with col1:
        st.markdown("### Project Mission")
        st.markdown("""
            <div class="kpi-card" style="padding: 24px; margin-bottom: 20px;">
                <div style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6;">
                    <strong>Nuroscan</strong> was conceived to demonstrate how state-of-the-art computer vision 
                    techniques can be translated into practical, transparent, and responsive clinical tools. 
                    <br/><br/>
                    Brain tumors are among the most aggressive oncological conditions, where timely diagnosis and precise 
                    anatomical localization can fundamentally change patient prognosis. By pairing <strong>YOLOv8</strong> object 
                    detection with an intuitive web workspace, Nuroscan provides sub-second localization across Glioma, 
                    Meningioma, and Pituitary adenomas.
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Core Technology Stack")
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.88rem;">
                    <div><strong>Deep Learning:</strong> PyTorch 2.0+</div>
                    <div><strong>Computer Vision:</strong> Ultralytics YOLOv8</div>
                    <div><strong>Backend API:</strong> FastAPI + Uvicorn</div>
                    <div><strong>Frontend UI:</strong> Streamlit Community</div>
                    <div><strong>Image Processing:</strong> Pillow + Headless OpenCV</div>
                    <div><strong>Visual Analytics:</strong> Plotly Graphs</div>
                    <div><strong>Containerization:</strong> Docker + Python 3.11</div>
                    <div><strong>Cloud Hosting:</strong> Render + Streamlit Cloud</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Developer & Project Links")
        st.markdown("""
            <div class="kpi-card" style="padding: 24px; margin-bottom: 20px;">
                <div style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">
                    Marwan Shafi
                </div>
                <div style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 16px;">
                    AI &amp; Software Engineer
                </div>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <a href="https://github.com/marwaaann/NeuroScan.AI" target="_blank" style="text-decoration: none;">
                        <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: var(--primary);">
                            🐙 GitHub: marwaaann/NeuroScan.AI ➔
                        </div>
                    </a>
                    <a href="https://neuroscan-ai-lp16.onrender.com" target="_blank" style="text-decoration: none;">
                        <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: var(--text-primary);">
                            🚀 Primary Cloud URL (Render) ➔
                        </div>
                    </a>
                    <a href="https://neuroscanai-ahwmpetaryjhq9pm3qv4et.streamlit.app" target="_blank" style="text-decoration: none;">
                        <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: var(--text-primary);">
                            ⚡ Streamlit Cloud URL ➔
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

    render_disclaimer()
    render_footer()
