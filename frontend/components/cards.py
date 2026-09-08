import streamlit as st
from typing import List, Optional

def render_top_header(title: str, description: str, meta_text: str = "", badges: Optional[List[str]] = None):
    """Render consistent clinical page header with typography and technology badges"""
    badge_html = ""
    if badges:
        badge_html = "<div class='header-badges-row'>" + "".join([f"<span class='tech-badge'>{b}</span>" for b in badges]) + "</div>"

    meta_html = f"<div class='header-meta' style='font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;'>{meta_text}</div>" if meta_text else ""

    st.markdown(f"""
        <div class="page-top-header">
            <div class="page-title">{title}</div>
            <div class="page-subtitle">{description}</div>
            {meta_html}
            {badge_html}
        </div>
    """, unsafe_allow_html=True)

def render_kpi_card(label: str, value: str, subtext: str = "", icon: str = "📊"):
    """Render modern clinical KPI statistic card with icon and elevation"""
    st.markdown(f"""
        <div class="kpi-card">
            <div>
                <div class="kpi-header">
                    <span class="kpi-label">{label}</span>
                    <div class="kpi-icon-pill">{icon}</div>
                </div>
                <div class="kpi-value">{value}</div>
            </div>
            <div class="kpi-subtext">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)

def render_workflow_steps(current_step: int = 1):
    """Render 4-step medical analysis visual progress bar"""
    steps = [
        (1, "Upload MRI"),
        (2, "AI Analysis"),
        (3, "Diagnostic Review"),
        (4, "Export Report")
    ]
    
    html = '<div class="workflow-stepper">'
    for idx, (step_num, step_name) in enumerate(steps):
        active_cls = "active" if step_num <= current_step else ""
        html += f'''
            <div class="step-item {active_cls}">
                <div class="step-number">{step_num}</div>
                <span>{step_name}</span>
            </div>
        '''
        if idx < len(steps) - 1:
            html += '<div class="step-divider"></div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def render_disclaimer():
    """Render restrained, authoritative medical research disclaimer"""
    st.markdown("""
        <div class="disclaimer-card">
            <div class="disclaimer-header">⚠️ Research &amp; Educational Tool — Not a Medical Diagnosis</div>
            <div class="disclaimer-body">
                Nuroscan provides deep learning bounding-box detection to assist scientific and educational research.
                Model inferences are probabilistic and must never replace diagnostic evaluation by a licensed physician or board-certified radiologist.
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render professional clinical healthcare footer inspired by NURA"""
    st.markdown("""
        <div class="footer-container">
            <div><strong>Nuroscan</strong> — AI Brain Health Screening &amp; Medical Vision Platform</div>
            <div style="margin-top: 4px; color: var(--text-muted);">
                Research by IIIT Sonepat (Rishabh, Marwan et al.) • YOLOv8 &amp; YOLOv11 Architectures
            </div>
            <div class="footer-links">
                <a href="https://github.com/marwaaann/NeuroScan.AI" target="_blank">GitHub Repository</a>
                <span>•</span>
                <a href="https://neuroscan-ai-lp16.onrender.com" target="_blank">Render Live Deployment</a>
                <span>•</span>
                <a href="https://neuroscanai-ahwmpetaryjhq9pm3qv4et.streamlit.app" target="_blank">Streamlit Cloud App</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
