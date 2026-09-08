import streamlit as st
from frontend.components.cards import render_top_header, render_disclaimer, render_footer

def render_how_it_works_page():
    """Render educational How It Works page explaining the YOLOv8 medical vision pipeline"""
    render_top_header(
        title="How NeuroScan AI Works",
        description="An overview of the deep learning computer-vision pipeline transforming raw MRI scans into diagnostic insights.",
        meta_text="Algorithm: YOLOv8 Single-Stage Detector • Spatial Resolution: 640×640",
        badges=["Deep Learning", "Convolutional Neural Network", "Feature Pyramid", "NMS Localization"]
    )

    st.markdown("""
        <div class="hero-banner-card" style="padding: 28px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: var(--text-primary); margin-bottom: 6px;">
                Single-Stage Object Detection in Medical Imaging
            </div>
            <div style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6;">
                Traditional two-stage detectors (like Faster R-CNN) first generate region proposals and then classify them sequentially. 
                <strong>YOLOv8</strong> operates as a single-stage neural network that predicts bounding coordinates and class probabilities 
                simultaneously across the entire image in a single forward pass, achieving real-time inference latency under 40 milliseconds.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### The 6-Stage Diagnostic Pipeline")

    stages = [
        ("1. Image Acquisition & Preprocessing", "🖼️", 
         "The uploaded MRI image (JPG, JPEG, or PNG) is ingested and normalized. It is resized to a standardized 640×640 RGB tensor matrix, and pixel intensities are scaled to [0, 1] for stable neural network inference."),
        ("2. DarkNet Backbone Feature Extraction", "🔬",
         "The tensor passes through successive convolutional layers (C2f modules) that extract multi-scale spatial features — ranging from low-level edges and textures to complex anatomical brain contours."),
        ("3. Feature Pyramid Network (PANet)", "📐",
         "A Path Aggregation Network combines semantic information across different scales. This ensures small early-stage micro-lesions and larger expansive tumors are detected with equal sensitivity."),
        ("4. Decoupled Prediction Heads", "⚡",
         "YOLOv8 employs decoupled heads that separate the task of bounding box regression (predicting coordinates x1, y1, x2, y2) from class probability estimation (Glioma, Meningioma, Pituitary, Normal)."),
        ("5. Non-Maximum Suppression (NMS)", "🎯",
         "Multiple overlapping candidate bounding boxes are evaluated. Non-Maximum Suppression filters redundant predictions and retains only the box with the highest confidence score."),
        ("6. Clinical Diagnostic Overlay & Export", "📊",
         "The bounding box is drawn over the original high-resolution MRI scan with color-coded classification tags and confidence percentages, ready for clinical review or report export.")
    ]

    for title, icon, desc in stages:
        st.markdown(f"""
            <div class="kpi-card" style="padding: 20px; margin-bottom: 12px;">
                <div style="display: flex; align-items: flex-start; gap: 14px;">
                    <div style="font-size: 1.8rem; line-height: 1;">{icon}</div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">{title}</div>
                        <div style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5;">{desc}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("### Human-in-the-Loop Clinical Paradigm")
    st.markdown("""
        <div class="kpi-card" style="padding: 24px;">
            <div style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6;">
                NeuroScan AI is strictly designed to function as an <strong>assistive second-reader tool</strong>. In a clinical workflow, 
                AI bounding boxes serve as an instant visual triage aid to draw the clinician's attention to suspicious tissue regions, 
                reducing diagnostic fatigue while keeping the final decision authority in the hands of the medical specialist.
            </div>
        </div>
    """, unsafe_allow_html=True)

    render_disclaimer()
    render_footer()
