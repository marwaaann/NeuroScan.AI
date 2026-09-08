import streamlit as st
import os
from PIL import Image

def get_verified_samples():
    """Locate verified sample MRI scans from the repository"""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    candidates = [
        {
            "id": "glioma",
            "name": "Glioma MRI Scan",
            "type_badge": "Glioma Lesion",
            "path": os.path.join(base_dir, "samples", "sample_glioma.jpg"),
            "description": "Axial T1-contrast scan displaying abnormal fronto-parietal region."
        },
        {
            "id": "scan1",
            "name": "Clinical Scan #1",
            "type_badge": "Evaluation MRI",
            "path": os.path.join(base_dir, "samples", "sample_scan_1.jpg"),
            "description": "Transverse brain scan evaluated against trained YOLOv8 model."
        },
        {
            "id": "scan2",
            "name": "Clinical Scan #2",
            "type_badge": "Evaluation MRI",
            "path": os.path.join(base_dir, "samples", "sample_scan_2.jpg"),
            "description": "Standard cranial magnetic resonance imaging slice."
        }
    ]
    
    return [c for c in candidates if os.path.exists(c["path"])]

def render_sample_selector():
    """Render modern visual cards for verified sample MRI scans"""
    samples = get_verified_samples()
    if not samples:
        return None

    st.markdown("""
        <div style="font-size: 0.88rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">
            Or Select a Pre-Loaded Verification Scan:
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(samples))
    selected_sample = None

    for idx, s in enumerate(samples):
        with cols[idx]:
            # Load thumbnail
            try:
                img = Image.open(s["path"])
                st.image(img, use_container_width=True)
            except Exception:
                pass
            
            st.markdown(f"""
                <div style="text-align: center; margin-top: 4px;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">{s['name']}</div>
                    <span class="sample-scan-badge">{s['type_badge']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Load {s['name'].split()[0]}", key=f"load_sample_{s['id']}", use_container_width=True, type="secondary"):
                selected_sample = s["path"]

    return selected_sample
