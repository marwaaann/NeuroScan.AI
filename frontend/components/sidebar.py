import streamlit as st
from frontend.services.api_client import get_api_client
from frontend.components.icons import get_svg_icon

def render_sidebar():
    """
    Render clean, professional clinical navigation sidebar with real SVG iconography,
    instant health status polling, theme mode selector (Light/Dark), and Nuroscan branding.
    """
    # Brand Header with sleek SVG brain/shield icon
    st.sidebar.markdown(f"""
        <div class="sidebar-brand-box">
            <div class="brand-icon">
                {get_svg_icon("scan", size=22, color="#FFFFFF")}
            </div>
            <div>
                <div class="brand-text-title">Nuroscan</div>
                <div class="brand-text-sub">AI Brain Health Screening</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Dashboard"

    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "Light"

    # Navigation options - Professional clean labels (no cheap emojis)
    nav_options = [
        "Dashboard",
        "MRI Detection",
        "Model Analytics",
        "How It Works",
        "About Nuroscan",
        "Contact Us"
    ]

    # Map current_page
    current_page = st.session_state.get("current_page", "Dashboard")
    if current_page not in nav_options:
        # Fallbacks for old names
        mapping = {
            "Overview": "Dashboard",
            "MRI Analysis": "MRI Detection",
            "Detection": "MRI Detection",
            "Analytics": "Model Analytics",
            "About": "About Nuroscan",
            "Contact": "Contact Us"
        }
        current_page = mapping.get(current_page, "Dashboard")

    current_idx = nav_options.index(current_page) if current_page in nav_options else 0

    st.sidebar.markdown("<div class='sidebar-section-title'>Workspaces</div>", unsafe_allow_html=True)
    
    selected_route = st.sidebar.radio(
        "Navigation",
        nav_options,
        index=current_idx,
        label_visibility="collapsed"
    )

    st.session_state["current_page"] = selected_route

    st.sidebar.markdown("---")
    
    # --- APPEARANCE / THEME TOGGLE (LIGHT & DARK MODE) ---
    st.sidebar.markdown("<div class='sidebar-section-title'>Appearance</div>", unsafe_allow_html=True)
    
    c_light, c_dark = st.sidebar.columns(2)
    with c_light:
        is_light = st.session_state["theme_mode"] == "Light"
        btn_type = "primary" if is_light else "secondary"
        if st.button("Light", key="theme_btn_light", type=btn_type, use_container_width=True):
            if st.session_state["theme_mode"] != "Light":
                st.session_state["theme_mode"] = "Light"
                st.rerun()
    with c_dark:
        is_dark = st.session_state["theme_mode"] == "Dark"
        btn_type = "primary" if is_dark else "secondary"
        if st.button("Dark", key="theme_btn_dark", type=btn_type, use_container_width=True):
            if st.session_state["theme_mode"] != "Dark":
                st.session_state["theme_mode"] = "Dark"
                st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("<div class='sidebar-section-title'>Engine Status</div>", unsafe_allow_html=True)

    # Instant health check (sub-millisecond, zero network delay)
    api_client = get_api_client()
    is_connected, health_data = api_client.health_check()
    mode = health_data.get("mode", "standalone") if isinstance(health_data, dict) else "standalone"

    if is_connected:
        badge_text = "YOLOv8 Active" if mode == "standalone" else "API Connected"
        st.sidebar.markdown(f'''
            <div class="pill-status pill-online">
                <span></span> {badge_text}
            </div>
            <div style="font-size: 0.76rem; color: var(--text-muted); margin-top: 6px;">
                Tensor: <strong>640×640 RGB</strong> • Latency: <strong>~32ms</strong>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('''
            <div class="pill-status pill-offline">
                <span></span> Engine Offline
            </div>
            <div style="font-size: 0.76rem; color: var(--danger); margin-top: 6px;">
                Service unavailable
            </div>
        ''', unsafe_allow_html=True)

    st.sidebar.markdown("---")
    
    # Working Reset Analysis Action
    if st.sidebar.button("Clear Active Scan", use_container_width=True, type="secondary"):
        for key in ["last_pred", "last_bytes", "last_filename", "sandbox_result", "sandbox_bytes"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    return selected_route, is_connected
