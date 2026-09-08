import streamlit as st

def render_login_page():
    """Render clinical researcher session management & profile portal"""
    st.markdown("""
        <div style="max-width: 480px; margin: 40px auto 0 auto; text-align: center;">
            <div class="brand-icon" style="margin: 0 auto 12px auto; width: 48px; height: 48px; font-size: 1.5rem;">N</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary); letter-spacing: -0.03em;">
                Clinical Research Session
            </div>
            <div style="font-size: 0.88rem; color: var(--text-secondary); margin-top: 4px; margin-bottom: 24px;">
                NeuroScan AI Diagnostic Workspace Access
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.8, 1])

    with col_m:
        st.markdown("""
            <div class="kpi-card" style="padding: 28px;">
        """, unsafe_allow_html=True)

        current_user = st.session_state.get("user_email", "researcher@neuroscan.ai")
        
        with st.form("researcher_session_form"):
            st.markdown("#### Active Clinical Account")
            new_email = st.text_input("Researcher Email", value=current_user)
            role = st.selectbox("Clinical Role", ["Medical Researcher", "Radiologist Fellow", "Diagnostic Specialist", "Clinical Reviewer"])
            
            st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
            save_btn = st.form_submit_button("Update Session & Enter Workspace ➔", type="primary", use_container_width=True)
            
            if save_btn:
                st.session_state["user_email"] = new_email or "researcher@neuroscan.ai"
                st.session_state["authenticated"] = True
                st.session_state["current_page"] = "Dashboard"
                st.rerun()

        st.markdown("""
            </div>
            <div style="text-align: center; margin-top: 16px;">
        """, unsafe_allow_html=True)
        
        if st.button("⬅ Return to Dashboard", type="secondary", use_container_width=True):
            st.session_state["authenticated"] = True
            st.session_state["current_page"] = "Dashboard"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
