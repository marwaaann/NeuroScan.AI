import streamlit as st
from frontend.components.cards import render_top_header, render_disclaimer, render_footer

def render_how_it_works_page():
    """
    Render educational How It Works page explaining the research-grade YOLO pipeline,
    based on the IIIT Sonepat study ('Brain Tumor Detection Using YOLOv8 and YOLOv11').
    """
    render_top_header(
        title="How Nuroscan Works — System Architecture",
        description="Comprehensive technical walkthrough of the deep learning pipeline transforming raw multi-planar MRI scans into localized diagnostic insights.",
        meta_text="Based on Research: IIIT Sonepat (Rishabh, Marwan et al.) • Multi-Perspective Cranial Imaging",
        badges=["YOLOv8 & YOLOv11", "Single-Stage Detection", "Bounding Box Regression", "92 FPS Real-Time"]
    )

    st.markdown("""
        <div class="hero-banner-card" style="padding: 30px;">
            <div style="font-size: 1.35rem; font-weight: 800; color: var(--navy-header); margin-bottom: 6px;">
                Single-Stage Multi-Planar Object Detection
            </div>
            <div style="font-size: 0.96rem; color: var(--text-secondary); line-height: 1.65;">
                Traditional CNNs (such as VGG16 or ResNet) perform whole-slice classification without indicating tumor coordinates, 
                while two-stage detectors (like Faster R-CNN) suffer from high latency. In contrast, <strong>YOLO</strong> 
                processes the entire cranial MRI scan in a single forward pass, predicting class probabilities and normalized bounding box coordinates 
                (<code>x_center</code>, <code>y_center</code>, <code>width</code>, <code>height</code>) simultaneously at <strong>92 FPS</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### The 6-Stage Research Methodology Pipeline")

    stages = [
        ("1. Multi-Planar MRI Acquisition & Standardization", "🖼️", 
         "Cranial scans from open-access repositories (including Kaggle Brain Tumor MRI Dataset) across three planes (axial, sagittal, coronal) are collected. All images are transformed from grayscale to standardized 640×640 RGB tensors."),
        ("2. Pixel Normalization & Gradient Stability", "⚖️",
         "Pixel intensity values are rescaled into the [0, 1] range. This prevents large gradient fluctuations during backpropagation, directing the model to learn structural morphology, texture, and boundary features rather than lighting variations."),
        ("3. Robust Data Augmentation & Balancing", "🔄",
         "Techniques including random horizontal/vertical flips, minor rotations (±15°), contrast adjustments, Gaussian noise injection, and minority class oversampling (e.g. for Pituitary adenomas) are applied to boost generalization on unseen scanner data."),
        ("4. Deep Feature Extraction (Backbone & PANet)", "🔬",
         "Multi-scale feature extraction combines spatial resolution with high-level contextual semantics, allowing detection of both minute incipient lesions and large compressive infiltrative tumors."),
        ("5. Decoupled Prediction Heads & NMS", "⚡",
         "Separate regression and classification heads output bounding coordinates and class confidence scores. Non-Maximum Suppression (NMS) eliminates overlapping duplicate proposals to isolate the true lesion boundary."),
        ("6. Clinical Diagnostic Overlay & Metric Export", "📊",
         "Real-time visual bounding box overlays are generated with color-coded classification tags (Glioma, Meningioma, Pituitary, Normal) along with confidence percentages and inference latency measurements.")
    ]

    for title, icon, desc in stages:
        st.markdown(f"""
            <div class="kpi-card" style="padding: 20px; margin-bottom: 12px;">
                <div style="display: flex; align-items: flex-start; gap: 14px;">
                    <div style="font-size: 1.8rem; line-height: 1;">{icon}</div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: var(--navy-header); margin-bottom: 4px;">{title}</div>
                        <div style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.55;">{desc}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown("### YOLOv8 vs YOLOv11 Architectural Comparison (From Research Paper)")
    st.markdown("""
        <div class="kpi-card" style="padding: 22px;">
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 2px solid var(--border-color); color: var(--navy-header);">
                            <th style="padding: 10px;">Metric / Attribute</th>
                            <th style="padding: 10px;">YOLOv8 Architecture</th>
                            <th style="padding: 10px; color: var(--primary);">YOLOv11 Architecture</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 10px; font-weight: 600;">Mean Average Precision (mAP)</td>
                            <td style="padding: 10px;">~0.93</td>
                            <td style="padding: 10px; color: var(--primary); font-weight: 700;">0.95 (Superior localization)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 10px; font-weight: 600;">Overall Precision</td>
                            <td style="padding: 10px;">94%</td>
                            <td style="padding: 10px; color: var(--primary); font-weight: 700;">96%</td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 10px; font-weight: 600;">Overall Recall / Sensitivity</td>
                            <td style="padding: 10px;">92%</td>
                            <td style="padding: 10px; color: var(--primary); font-weight: 700;">94%</td>
                        </tr>
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 10px; font-weight: 600;">Real-Time Inference Speed</td>
                            <td style="padding: 10px;">~80 FPS</td>
                            <td style="padding: 10px; color: var(--primary); font-weight: 700;">92 FPS (Ultra-fast)</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: 600;">Deployment In Nuroscan</td>
                            <td style="padding: 10px; font-weight: 600; color: var(--success);">Active Production Model</td>
                            <td style="padding: 10px;">Research Benchmark Target</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    """, unsafe_allow_html=True)

    render_disclaimer()
    render_footer()
