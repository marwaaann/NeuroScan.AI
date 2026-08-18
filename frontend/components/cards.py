import streamlit as st

def render_top_header(title: str, description: str, meta_text: str = ""):
    """Render consistent page header across all sections"""
    st.markdown(f"""
        <div class="header-title">{title}</div>
        <div class="header-description">{description}</div>
        {f'<div class="header-meta">{meta_text}</div>' if meta_text else ''}
        <br/>
    """, unsafe_allow_html=True)

def render_stat_card(label: str, value: str, subtext: str = ""):
    """Render crisp statistic card"""
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label-text">{label}</div>
            <div class="metric-value-text">{value}</div>
            {f'<div class="metric-sub-text">{subtext}</div>' if subtext else ''}
        </div>
    """, unsafe_allow_html=True)

def render_disclaimer():
    """Render restrained, professional medical research disclaimer"""
    st.markdown("""
        <div class="disclaimer-box">
            <strong>Research & Educational Use Only</strong><br/>
            NeuroScan AI is a computer-vision research prototype. Model predictions are probabilistic 
            and are not a medical diagnosis or substitute for evaluation by a qualified healthcare professional.
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render minimal footer"""
    st.markdown("""
        <div class="footer-text">
            <strong>NeuroScan AI</strong> — AI-assisted Brain MRI Analysis<br/>
            Research & Educational Prototype • YOLOv8 • FastAPI • Streamlit
        </div>
    """, unsafe_allow_html=True)
