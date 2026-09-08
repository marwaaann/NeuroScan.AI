import sys
import os

# Ensure repository root is in sys.path so 'frontend' and 'backend' packages resolve cleanly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

# ---------------------------------------------------------
# Page Configuration & Custom Favicon
# ---------------------------------------------------------
FAVICON_PATH = os.path.join(os.path.dirname(__file__), "favicon.png")
page_icon_val = FAVICON_PATH if os.path.exists(FAVICON_PATH) else None

st.set_page_config(
    page_title="Nuroscan | Clinical Brain MRI Platform",
    page_icon=page_icon_val,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Load CSS Theme System & Dynamic Appearance Injection
# ---------------------------------------------------------
CSS_PATH = os.path.join(os.path.dirname(__file__), "styles", "theme.css")
if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Dynamic Dark Mode Support
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Light"

if st.session_state["theme_mode"] == "Dark":
    st.markdown("""
        <style>
            :root, .stApp, section[data-testid="stSidebar"] {
                --bg-main: #0A1118 !important;
                --bg-sidebar: #0D1622 !important;
                --surface-card: #131E2C !important;
                --surface-elevated: #1A283A !important;
                --surface-subtle: #101924 !important;
                --border-color: #223447 !important;
                --border-highlight: #33485E !important;
                --border-medical: rgba(0, 191, 165, 0.3) !important;
                
                --text-primary: #F0F6FC !important;
                --text-secondary: #94A3B8 !important;
                --text-muted: #64748B !important;
                --navy-header: #F0F6FC !important;
                
                --primary: #00BFA5 !important;
                --primary-hover: #1DE9B6 !important;
                --primary-dark: #00897B !important;
                --primary-light: rgba(0, 191, 165, 0.18) !important;
                --primary-glow: rgba(0, 191, 165, 0.3) !important;
                
                --accent-teal: #2DD4BF !important;
                --accent-teal-light: rgba(45, 212, 191, 0.15) !important;
                --accent-cyan: #38BDF8 !important;
                --accent-cyan-light: rgba(56, 189, 248, 0.15) !important;
                
                background-color: #0A1118 !important;
                color: #F0F6FC !important;
            }
            .hero-banner-card {
                background: linear-gradient(135deg, #0F202B 0%, #131E2C 50%, #0D1B28 100%) !important;
                border-color: rgba(0, 191, 165, 0.25) !important;
            }
            .nura-contact-card {
                background: linear-gradient(135deg, #0D2028 0%, #131E2C 100%) !important;
                border-color: rgba(0, 191, 165, 0.25) !important;
            }
            .kpi-card, .image-panel-card, .disclaimer-card, .result-banner-box {
                background-color: #131E2C !important;
                border-color: #223447 !important;
            }
            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea,
            div[data-testid="stSelectbox"] > div > div {
                background-color: #131E2C !important;
                border-color: #223447 !important;
                color: #F0F6FC !important;
            }
            .tech-badge {
                background-color: #1A283A !important;
                border-color: #223447 !important;
                color: #CBD5E1 !important;
            }
        </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Modular Page Imports (Clean & Essential)
# ---------------------------------------------------------
from frontend.components.sidebar import render_sidebar
from frontend.pages.overview import render_overview_page
from frontend.pages.detection import render_detection_page
from frontend.pages.analytics import render_analytics_page
from frontend.pages.how_it_works import render_how_it_works_page
from frontend.pages.about import render_about_page
from frontend.pages.contact import render_contact_page

def main():
    # Session state initialization - Direct Access by Default
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Dashboard"

    if "scan_history" not in st.session_state:
        st.session_state["scan_history"] = []

    # Render main clinical shell & sidebar
    selected_page, is_api_connected = render_sidebar()

    # Route to appropriate clinical view
    if selected_page in ["Dashboard", "Overview"]:
        render_overview_page(is_api_connected)
    elif selected_page in ["MRI Detection", "MRI Analysis", "Detection"]:
        render_detection_page(is_api_connected)
    elif selected_page in ["Model Analytics", "Analytics"]:
        render_analytics_page()
    elif selected_page in ["How It Works"]:
        render_how_it_works_page()
    elif selected_page in ["About Nuroscan", "About"]:
        render_about_page()
    elif selected_page in ["Contact Us", "Contact"]:
        render_contact_page()
    else:
        render_overview_page(is_api_connected)

if __name__ == "__main__":
    main()
