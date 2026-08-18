import streamlit as st

def render_login_page():
    """Render clean light-blue unified login portal — Orshot-style"""

    st.markdown("""
        <style>
        /* =============================================
           LOGIN PAGE — LIGHT UNIFIED BLUE-WHITE THEME
           One surface, no box-in-box, clean & minimal
           ============================================= */

        /* Full page light blue-white background — matches website accent */
        .stApp {
            background: #EEF4FF !important;
        }
        .stApp > div, .block-container {
            background: transparent !important;
        }

        /* Hide Streamlit chrome */
        header[data-testid="stHeader"],
        #MainMenu, footer,
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* Center the whole page content */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            max-width: 100% !important;
        }

        /* Login card — white, blends with light bg */
        .login-card-clean {
            background: #FFFFFF;
            border: 1px solid #DBEAFE;
            border-radius: 16px;
            padding: 44px 40px 36px 40px;
            max-width: 420px;
            margin: 0 auto;
            box-shadow:
                0 1px 3px rgba(59, 130, 246, 0.06),
                0 8px 28px rgba(59, 130, 246, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.04);
        }

        /* Input label */
        label[data-testid="stWidgetLabel"] p,
        label[data-testid="stWidgetLabel"] {
            color: #374151 !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.025em !important;
        }

        /* Input field — very light grey, clean */
        div[data-baseweb="input"] > div {
            background-color: #F3F6FF !important;
            border: 1.5px solid #DBEAFE !important;
            border-radius: 9px !important;
            box-shadow: none !important;
            transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        }
        div[data-baseweb="input"] > div:focus-within {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12) !important;
            background-color: #FFFFFF !important;
        }
        div[data-baseweb="input"] input {
            color: #111827 !important;
            background: transparent !important;
            font-weight: 500 !important;
            font-size: 0.93rem !important;
        }
        div[data-baseweb="input"] input::placeholder {
            color: #9CA3AF !important;
        }
        div[data-baseweb="input"] button {
            color: #9CA3AF !important;
        }
        div[data-baseweb="input"] button:hover {
            color: #6B7280 !important;
        }

        /* Submit button — website blue */
        div[data-testid="stFormSubmitButton"] button,
        div.stFormSubmitButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 0.93rem !important;
            border-radius: 9px !important;
            padding: 12px 20px !important;
            box-shadow: 0 2px 12px rgba(37, 99, 235, 0.3) !important;
            transition: all 0.15s ease !important;
            margin-top: 6px !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover,
        div.stFormSubmitButton > button:hover {
            background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%) !important;
            box-shadow: 0 4px 18px rgba(59, 130, 246, 0.45) !important;
            transform: translateY(-1px) !important;
        }

        /* Form — no border/bg */
        div[data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        /* Error alert */
        div[data-testid="stAlert"] {
            background-color: rgba(239, 68, 68, 0.06) !important;
            border: 1px solid rgba(239, 68, 68, 0.2) !important;
            border-radius: 8px !important;
            color: #DC2626 !important;
        }

        /* Thin divider */
        .ln-divider {
            height: 1px;
            background: #EEF2FF;
            margin: 20px 0;
        }

        /* Footer note */
        .login-footer-note {
            text-align: center;
            color: #9CA3AF;
            font-size: 0.74rem;
            margin-top: 18px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Vertical centering spacer
    st.markdown("<div style='height: 80px'></div>", unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.6, 1])

    with col_m:
        # Card header
        st.markdown("""
            <div class="login-card-clean">
                <div style="text-align: center; margin-bottom: 26px;">
                    <div style="
                        width: 50px; height: 50px;
                        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
                        border-radius: 13px;
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.5rem;
                        font-weight: 900;
                        color: #fff;
                        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35);
                        letter-spacing: -0.04em;
                        margin-bottom: 16px;
                    ">N</div>
                    <div style="
                        font-size: 1.45rem;
                        font-weight: 800;
                        color: #111827;
                        letter-spacing: -0.03em;
                        margin-bottom: 6px;
                    ">
                        NeuroScan<span style="color:#2563EB">.AI</span>
                    </div>
                    <div style="font-size: 0.84rem; color: #6B7280;">
                        Brain MRI Tumor Detection Platform
                    </div>
                </div>
                <div class="ln-divider"></div>
            </div>
        """, unsafe_allow_html=True)

        # Streamlit form
        with st.form("demo_login_form", clear_on_submit=False):
            email = st.text_input(
                "Email / Username",
                value="researcher@neuroscan.ai",
                placeholder="Enter your email"
            )
            password = st.text_input(
                "Password",
                type="password",
                value="neuro2026",
                placeholder="Enter your password"
            )

            st.markdown("<div style='height: 4px'></div>", unsafe_allow_html=True)

            submit_btn = st.form_submit_button(
                "Enter Workspace  →",
                use_container_width=True,
                type="primary"
            )

            if submit_btn:
                if email and password:
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.rerun()
                else:
                    st.error("Please enter a valid email and password.")

        st.markdown("""
            <div class="login-footer-note">
                🔒 &nbsp;Research &amp; Educational Use Only &nbsp;·&nbsp; YOLOv8 Powered
            </div>
        """, unsafe_allow_html=True)

    st.stop()
