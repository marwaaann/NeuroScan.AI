import streamlit as st
from frontend.services.api_client import get_api_client

def render_sidebar():
    """
    Render grouped, clinical-grade navigation sidebar with real-time health indicator,
    organized workspaces, and active researcher profile.
    """
    # Brand Header
    st.sidebar.markdown("""
        <div class="sidebar-brand-box">
            <div class="brand-icon">N</div>
            <div>
                <div class="brand-text-title">NeuroScan<span class="brand-text-accent">.AI</span></div>
                <div class="brand-text-sub">Brain MRI Vision Platform</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Dashboard"

    # Navigation mapping
    nav_labels = [
        "📊 Dashboard",
        "🔬 MRI Analysis",
        "📁 Scan History",
        "📈 Model Analytics",
        "⚙️ Technical Specs",
        "💡 How It Works",
        "ℹ️ About NeuroScan"
    ]

    # Map current_page to full label
    label_map = {
        "Dashboard": "📊 Dashboard",
        "Overview": "📊 Dashboard",
        "MRI Analysis": "🔬 MRI Analysis",
        "Detection": "🔬 MRI Analysis",
        "Scan History": "📁 Scan History",
        "Model Analytics": "📈 Model Analytics",
        "Technical Specs": "⚙️ Technical Specs",
        "Model Information": "⚙️ Technical Specs",
        "How It Works": "💡 How It Works",
        "About NeuroScan": "ℹ️ About NeuroScan",
        "About": "ℹ️ About NeuroScan"
    }

    current_label = label_map.get(st.session_state["current_page"], "📊 Dashboard")
    current_idx = nav_labels.index(current_label) if current_label in nav_labels else 0

    st.sidebar.markdown("<div class='sidebar-section-title'>Workspaces</div>", unsafe_allow_html=True)
    
    selected_label = st.sidebar.radio(
        "Navigation",
        nav_labels,
        index=current_idx,
        label_visibility="collapsed"
    )

    # Reverse mapping to clean route names
    clean_map = {
        "📊 Dashboard": "Dashboard",
        "🔬 MRI Analysis": "MRI Analysis",
        "📁 Scan History": "Scan History",
        "📈 Model Analytics": "Model Analytics",
        "⚙️ Technical Specs": "Technical Specs",
        "💡 How It Works": "How It Works",
        "ℹ️ About NeuroScan": "About NeuroScan"
    }
    
    selected_route = clean_map.get(selected_label, "Dashboard")
    st.session_state["current_page"] = selected_route

    st.sidebar.markdown("---")
    st.sidebar.markdown("<div class='sidebar-section-title'>System &amp; Engine</div>", unsafe_allow_html=True)

    # Health polling
    api_client = get_api_client()
    is_connected, health_data = api_client.health_check()
    mode = health_data.get("mode", "api") if isinstance(health_data, dict) else "api"

    if is_connected:
        badge_text = "Connected (API)" if mode == "api" else "Active (Standalone YOLO)"
        st.sidebar.markdown(f'<div class="pill-status pill-online"><span></span> {badge_text}</div>', unsafe_allow_html=True)
        st.sidebar.markdown("""
            <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 6px;">
                Engine: <strong>YOLOv8n PyTorch</strong> (640×640)
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div class="pill-status pill-offline"><span></span> Engine Offline</div>', unsafe_allow_html=True)
        st.sidebar.markdown("""
            <div style="font-size: 0.76rem; color: var(--danger); margin-top: 6px;">
                Service unavailable
            </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("<div class='sidebar-section-title'>Researcher Session</div>", unsafe_allow_html=True)

    user_email = st.session_state.get("user_email", "researcher@neuroscan.ai")
    initial = user_email[0].upper() if user_email else "R"

    st.sidebar.markdown(f"""
        <div class="researcher-session-card">
            <div class="researcher-avatar">{initial}</div>
            <div style="overflow: hidden;">
                <div style="font-size: 0.82rem; font-weight: 700; color: var(--text-primary); text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                    {user_email}
                </div>
                <div style="font-size: 0.7rem; color: var(--primary); font-weight: 600;">Clinical Demo Session</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("Reset Analysis Session", use_container_width=True, type="secondary"):
        if "last_pred" in st.session_state:
            del st.session_state["last_pred"]
        if "last_bytes" in st.session_state:
            del st.session_state["last_bytes"]
        if "last_filename" in st.session_state:
            del st.session_state["last_filename"]
        st.rerun()

    return selected_route, is_connected
