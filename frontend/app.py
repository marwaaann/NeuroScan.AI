import streamlit as st
import os

# ---------------------------------------------------------
# Page Configuration & Custom Favicon
# ---------------------------------------------------------
FAVICON_PATH = os.path.join(os.path.dirname(__file__), "favicon.png")
page_icon_val = FAVICON_PATH if os.path.exists(FAVICON_PATH) else "🧠"

st.set_page_config(
    page_title="NeuroScan AI | Research Workspace",
    page_icon=page_icon_val,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Theme System
CSS_PATH = os.path.join(os.path.dirname(__file__), "styles", "theme.css")
if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Imports after page config
from frontend.pages.login import render_login_page
from frontend.components.sidebar import render_sidebar
from frontend.pages.overview import render_overview_page
from frontend.pages.detection import render_detection_page
from frontend.pages.analytics import render_analytics_page
from frontend.pages.model_info import render_model_info_page

def main():
    # Session state authentication gate
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        render_login_page()
        return

    # Render main workspace
    selected_page, is_api_connected = render_sidebar()

    if selected_page == "Overview":
        render_overview_page(is_api_connected)
    elif selected_page == "Detection":
        render_detection_page(is_api_connected)
    elif selected_page == "Model Analytics":
        render_analytics_page()
    elif selected_page == "Model Information":
        render_model_info_page()

if __name__ == "__main__":
    main()
