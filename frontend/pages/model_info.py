import streamlit as st
import os

from frontend.components.cards import render_top_header, render_stat_card, render_disclaimer, render_footer

def render_model_info_page():
    render_top_header(
        title="Model Information",
        description="Technical specifications, class mapping, and system architecture."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Technical Specifications")
        st.markdown("""
            <div class="ns-surface-card">
                <div style="margin-bottom: 10px;">
                    <strong style="color: var(--text-primary);">Model:</strong> YOLOv8n (Nano)
                </div>
                <div style="margin-bottom: 10px;">
                    <strong style="color: var(--text-primary);">Framework:</strong> PyTorch + Ultralytics
                </div>
                <div style="margin-bottom: 10px;">
                    <strong style="color: var(--text-primary);">Task:</strong> 2D Object Detection
                </div>
                <div style="margin-bottom: 10px;">
                    <strong style="color: var(--text-primary);">Input Matrix:</strong> 640 × 640 RGB
                </div>
                <div>
                    <strong style="color: var(--text-primary);">Weights File:</strong> <code>model/best.pt</code>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### Target Classes")
        st.markdown("""
            | Class ID | Class Name | Description |
            | :--- | :--- | :--- |
            | `0` | **Glioma** | Primary tumor originating in glial cells |
            | `1` | **Meningioma** | Tumor arising from brain membranes |
            | `2` | **No Tumor** | Normal MRI scan without tumor lesions |
            | `3` | **Pituitary** | Tumor located in pituitary gland |
        """)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### System Architecture Pipeline")

    st.markdown("""
        <div class="ns-surface-card" style="padding: 24px;">
            <div style="display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; gap: 8px; font-weight: 600; font-size: 0.88rem;">
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 6px;">MRI Image</div>
                <div style="color: var(--primary-accent);">↓</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 6px;">Streamlit UI (Frontend)</div>
                <div style="color: var(--primary-accent);">↓</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 6px;">HTTP POST</div>
                <div style="color: var(--primary-accent);">↓</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 6px;">FastAPI (Backend)</div>
                <div style="color: var(--primary-accent);">↓</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 6px;">YOLOv8 best.pt</div>
                <div style="color: var(--primary-accent);">↓</div>
                <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 6px;">JSON Result</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    yaml_path = os.path.join(os.getcwd(), "brain_tumor_dataset.yaml")
    if os.path.exists(yaml_path):
        st.markdown("### Dataset Configuration (`brain_tumor_dataset.yaml`)")
        with open(yaml_path, "r") as f:
            st.code(f.read(), language="yaml")

    render_disclaimer()
    render_footer()
