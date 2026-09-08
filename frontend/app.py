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
page_icon_val = FAVICON_PATH if os.path.exists(FAVICON_PATH) else "🧠"

st.set_page_config(
    page_title="Nuroscan | Clinical Brain MRI Platform",
    page_icon=page_icon_val,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Load CSS Theme System
# ---------------------------------------------------------
CSS_PATH = os.path.join(os.path.dirname(__file__), "styles", "theme.css")
if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Modular Page Imports (Clean & Essential)
# ---------------------------------------------------------
from frontend.components.sidebar import render_sidebar
from frontend.pages.overview import render_overview_page
from frontend.pages.detection import render_detection_page
from frontend.pages.analytics import render_analytics_page
from frontend.pages.how_it_works import render_how_it_works_page
from frontend.pages.about import render_about_page

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
    else:
        render_overview_page(is_api_connected)

if __name__ == "__main__":
    main()
