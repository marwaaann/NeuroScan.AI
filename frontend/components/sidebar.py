import streamlit as st
from frontend.services.api_client import get_api_client

def render_sidebar():
    """Render compact, persistent left navigation sidebar"""
    st.sidebar.markdown("""
        <div class="sidebar-header">
            <div class="brand-logo-container" style="margin-bottom: 4px;">
                <div class="brand-logo-icon">N</div>
                <div class="brand-logo-text">NeuroScan<span class="brand-logo-accent">.AI</span></div>
            </div>
            <div class="sidebar-brand-subtitle">AI Brain MRI Analysis</div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("<span style='font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;'>Workspace</span>", unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Overview"

    nav_options = ["Overview", "Detection", "Model Analytics", "Model Information"]
    curr_idx = nav_options.index(st.session_state.get("current_page", "Overview")) if st.session_state.get("current_page") in nav_options else 0

    selected_nav = st.sidebar.radio(
        "Workspace Navigation",
        nav_options,
        index=curr_idx,
        label_visibility="collapsed"
    )
    st.session_state["current_page"] = selected_nav

    st.sidebar.markdown("---")
    st.sidebar.markdown("<span style='font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;'>System</span>", unsafe_allow_html=True)

    # Real health polling via API Client
    api_client = get_api_client()
    is_connected, health_data = api_client.health_check()

    st.sidebar.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 4px;'>API Status</div>", unsafe_allow_html=True)
    if is_connected:
        st.sidebar.markdown('<div class="pill-online"><span>●</span> Connected</div>', unsafe_allow_html=True)
        st.sidebar.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: var(--text-secondary); margin-top: 10px; margin-bottom: 4px;'>Model Status</div>", unsafe_allow_html=True)
        st.sidebar.markdown('<div style="font-size: 0.8rem; font-weight: 600; color: var(--text-primary);">YOLOv8n Loaded</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div class="pill-offline"><span>●</span> Offline</div>', unsafe_allow_html=True)
        st.sidebar.markdown("<div style='font-size: 0.8rem; font-weight: 600; color: var(--text-secondary); margin-top: 10px; margin-bottom: 4px;'>Model Status</div>", unsafe_allow_html=True)
        st.sidebar.markdown('<div style="font-size: 0.8rem; font-weight: 600; color: var(--error-color);">Unavailable</div>', unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # User Session Card & Logout Button
    user_email = st.session_state.get("user_email", "researcher@neuroscan.ai")
    st.sidebar.markdown(f"""
        <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); border-radius: 6px; padding: 10px 12px; margin-bottom: 12px;">
            <div style="font-weight: 600; font-size: 0.82rem; color: var(--text-primary); text-overflow: ellipsis; overflow: hidden;">{user_email}</div>
            <div style="font-size: 0.72rem; color: var(--primary-accent); font-weight: 600;">Research Session</div>
        </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("Logout Workspace", use_container_width=True, type="secondary"):
        st.session_state["authenticated"] = False
        if "last_pred" in st.session_state:
            del st.session_state["last_pred"]
        st.rerun()

    return selected_nav, is_connected
