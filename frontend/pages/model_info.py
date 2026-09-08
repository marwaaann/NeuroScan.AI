import streamlit as st
import os
from frontend.components.cards import render_top_header, render_disclaimer, render_footer

def render_model_info_page():
    """Render comprehensive Technical Specifications and Architecture page"""
    render_top_header(
        title="Technical Specifications & Architecture",
        description="Deep learning specifications, classification reference, and architectural engineering.",
        meta_text="Framework: PyTorch • Model: YOLOv8n • Weights: model/best.pt",
        badges=["PyTorch Engine", "DarkNet FPN", "640×640 Matrix"]
    )

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("### Model Specifications")
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="margin-bottom: 12px; display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">Architecture</span>
                    <strong style="color: var(--text-primary);">Ultralytics YOLOv8n (Nano)</strong>
                </div>
                <div style="margin-bottom: 12px; display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">Core Framework</span>
                    <strong style="color: var(--text-primary);">PyTorch + Torchvision</strong>
                </div>
                <div style="margin-bottom: 12px; display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">Vision Task</span>
                    <strong style="color: var(--text-primary);">2D Bounding-Box Localization</strong>
                </div>
                <div style="margin-bottom: 12px; display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">Input Resolution</span>
                    <strong style="color: var(--text-primary);">640 × 640 RGB Tensor</strong>
                </div>
                <div style="display: flex; justify-content: space-between; padding-top: 4px;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">Weights Location</span>
                    <strong style="color: var(--primary);"><code>model/best.pt</code> (6.2 MB)</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### Target Tumor Classifications")
        st.markdown("""
            | Class ID | Tumor Label | Clinical Description |
            | :---: | :--- | :--- |
            | `0` | **Glioma** | Primary tumor arising from glial cells in the brain or spinal cord |
            | `1` | **Meningioma** | Typically slow-growing tumor originating in the meningeal membranes |
            | `2` | **No Tumor** | Normal cranial MRI scan displaying healthy brain parenchyma |
            | `3` | **Pituitary** | Neoplasm developing within the pituitary gland at the skull base |
        """)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### Dual-Execution Architectural Pipeline")

    st.markdown("""
        <div class="kpi-card" style="padding: 28px;">
            <div style="display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; gap: 12px; font-weight: 600; font-size: 0.86rem; text-align: center;">
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 1.2rem; margin-bottom: 4px;">🖼️</div>
                    MRI Scan (JPG/PNG)
                </div>
                <div style="color: var(--primary); font-size: 1.2rem;">➔</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 1.2rem; margin-bottom: 4px;">💻</div>
                    Streamlit Frontend
                </div>
                <div style="color: var(--primary); font-size: 1.2rem;">➔</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 1.2rem; margin-bottom: 4px;">⚡</div>
                    FastAPI / Standalone Fallback
                </div>
                <div style="color: var(--primary); font-size: 1.2rem;">➔</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 1.2rem; margin-bottom: 4px;">🧠</div>
                    YOLOv8 best.pt
                </div>
                <div style="color: var(--primary); font-size: 1.2rem;">➔</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 1.2rem; margin-bottom: 4px;">📊</div>
                    Diagnostic JSON + Overlay
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Optional Dataset YAML Inspection
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yaml_candidates = [
        os.path.join(base_dir, "training", "brain_tumor_dataset.yaml"),
        os.path.join(base_dir, "brain_tumor_dataset.yaml")
    ]
    for yp in yaml_candidates:
        if os.path.exists(yp):
            with st.expander("📄 View Dataset Configuration (`brain_tumor_dataset.yaml`)"):
                with open(yp, "r") as f:
                    st.code(f.read(), language="yaml")
            break

    render_disclaimer()
    render_footer()
