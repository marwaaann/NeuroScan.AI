import streamlit as st
from frontend.services.api_client import get_api_client

def render_sidebar():
    """
    Render clean, streamlined clinical navigation sidebar with real-time health indicator,
    essential workspaces, and Nuroscan branding.
    """
    # Brand Header
    st.sidebar.markdown("""
        <div class="sidebar-brand-box">
            <div class="brand-icon">N</div>
            <div>
                <div class="brand-text-title">Nuroscan</div>
                <div class="brand-text-sub">AI Brain MRI Platform</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Dashboard"

    # Navigation options - Essential & focused
    nav_labels = [
        "📊 Dashboard",
        "🔬 MRI Detection",
        "📈 Model Analytics",
        "💡 How It Works",
        "ℹ️ About Nuroscan"
    ]

    # Map current_page to full label
    label_map = {
        "Dashboard": "📊 Dashboard",
        "Overview": "📊 Dashboard",
        "MRI Detection": "🔬 MRI Detection",
        "MRI Analysis": "🔬 MRI Detection",
        "Detection": "🔬 MRI Detection",
        "Model Analytics": "📈 Model Analytics",
        "Analytics": "📈 Model Analytics",
        "How It Works": "💡 How It Works",
        "About Nuroscan": "ℹ️ About Nuroscan",
        "About": "ℹ️ About Nuroscan"
    }

    current_label = label_map.get(st.session_state["current_page"], "📊 Dashboard")
    current_idx = nav_labels.index(current_label) if current_label in nav_labels else 0

    st.sidebar.markdown("<div class='sidebar-section-title'>Navigation</div>", unsafe_allow_html=True)
    
    selected_label = st.sidebar.radio(
        "Navigation",
        nav_labels,
        index=current_idx,
        label_visibility="collapsed"
    )

    # Clean route mapping
    clean_map = {
        "📊 Dashboard": "Dashboard",
        "🔬 MRI Detection": "MRI Detection",
        "📈 Model Analytics": "Model Analytics",
        "💡 How It Works": "How It Works",
        "ℹ️ About Nuroscan": "About Nuroscan"
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
        badge_text = "API Connected" if mode == "api" else "YOLOv8 Active"
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
    
    # Quick Reset Analysis
    if st.sidebar.button("🔄 Reset Scan State", use_container_width=True, type="secondary"):
        for key in ["last_pred", "last_bytes", "last_filename"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    return selected_route, is_connected
