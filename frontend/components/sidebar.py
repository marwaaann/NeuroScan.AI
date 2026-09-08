import streamlit as st
from frontend.services.api_client import get_api_client
from frontend.components.icons import get_svg_icon

def render_sidebar():
    """
    Render clean, professional clinical navigation sidebar with real SVG iconography,
    instant health status polling, and NeuroScan.AI branding.
    """
    # Brand Header with sleek SVG brain/shield icon
    st.sidebar.markdown(f"""
        <div class="sidebar-brand-box">
            <div class="brand-icon">
                {get_svg_icon("scan", size=22, color="#FFFFFF")}
            </div>
            <div>
                <div class="brand-text-title">NeuroScan.AI</div>
                <div class="brand-text-sub">AI Brain Health Screening</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Dashboard"

    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "Light"

    # Navigation items - Real clinical icons via Google Material Symbols (no emojis, no radio circles)
    nav_items = [
        ("Dashboard", ":material/dashboard:"),
        ("MRI Detection", ":material/radiology:"),
        ("Model Analytics", ":material/analytics:"),
        ("How It Works", ":material/account_tree:"),
        ("About NeuroScan.AI", ":material/description:"),
        ("Contact Us", ":material/support_agent:")
    ]

    # Map current_page
    current_page = st.session_state.get("current_page", "Dashboard")
    nav_names = [item[0] for item in nav_items]
    if current_page not in nav_names:
        mapping = {
            "Overview": "Dashboard",
            "MRI Analysis": "MRI Detection",
            "Detection": "MRI Detection",
            "Analytics": "Model Analytics",
            "About": "About NeuroScan.AI",
            "About Nuroscan": "About NeuroScan.AI",
            "Contact": "Contact Us"
        }
        current_page = mapping.get(current_page, "Dashboard")
        st.session_state["current_page"] = current_page

    PAGE_SLUGS = {
        "Dashboard": "dashboard",
        "MRI Detection": "detection",
        "Model Analytics": "analytics",
        "How It Works": "how-it-works",
        "About NeuroScan.AI": "about",
        "Contact Us": "contact"
    }

    st.sidebar.markdown("<div class='sidebar-section-title'>Workspaces</div>", unsafe_allow_html=True)
    
    for page_name, icon_spec in nav_items:
        is_active = (current_page == page_name)
        btn_type = "primary" if is_active else "secondary"
        if st.sidebar.button(
            page_name,
            icon=icon_spec,
            key=f"nav_btn_{page_name.replace(' ', '_').replace('.', '_')}",
            type=btn_type,
            use_container_width=True
        ):
            if st.session_state.get("current_page") != page_name:
                st.session_state["current_page"] = page_name
                try:
                    st.query_params["page"] = PAGE_SLUGS.get(page_name, "dashboard")
                except Exception:
                    pass
                st.rerun()

    selected_route = st.session_state.get("current_page", "Dashboard")
    try:
        st.query_params["page"] = PAGE_SLUGS.get(selected_route, "dashboard")
    except Exception:
        pass

    st.sidebar.markdown("---")
    st.sidebar.markdown("<div class='sidebar-section-title'>Engine Status</div>", unsafe_allow_html=True)

    # Instant health check (sub-millisecond, zero network delay)
    api_client = get_api_client()
    is_connected, health_data = api_client.health_check()
    mode = health_data.get("mode", "standalone") if isinstance(health_data, dict) else "standalone"

    if is_connected:
        badge_text = "YOLOv8 Active" if mode in ["standalone", "in-process"] else "API Connected"
        st.sidebar.markdown(f'''
            <div class="pill-status pill-online">
                <span></span> {badge_text}
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

    return selected_route, is_connected

