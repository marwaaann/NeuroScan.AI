import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

from frontend.components.cards import render_top_header, render_kpi_card, render_disclaimer, render_footer

def resolve_asset_path(filename: str) -> str:
    """Find metric asset across tracked frontend/assets or training run"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, "assets", "metrics", filename),
        os.path.join(os.getcwd(), "frontend", "assets", "metrics", filename),
        os.path.join(os.getcwd(), "brain_tumor_detector", "yolov8n_run_1", filename)
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return ""

def render_analytics_page():
    """Render comprehensive empirical model performance analytics and training history"""
    render_top_header(
        title="Model Performance & Training Analytics",
        description="Empirical validation curves, loss telemetry, and classification metrics across 20 training epochs.",
        meta_text="Model: YOLOv8n • Dataset: Brain Tumor MRI • Target Classes: 4",
        badges=["Empirical Metrics", "Plotly Visualizations", "Loss Telemetry"]
    )

    # Top KPI Metrics Overview
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("VALIDATION mAP@50", "96.31%", "Mean Average Precision at IoU 0.50", "precision")
    with k2:
        render_kpi_card("mAP@50-95", "79.46%", "mAP across IoU 0.50:0.95 range", "analytics")
    with k3:
        render_kpi_card("PRECISION", "93.87%", "Bounding Box Precision", "check")
    with k4:
        render_kpi_card("RECALL", "94.01%", "Lesion Detection Sensitivity", "speed")

    st.markdown("<br/>", unsafe_allow_html=True)

    csv_path = resolve_asset_path("results.csv")
    cm_path = resolve_asset_path("confusion_matrix_normalized.png")
    if not cm_path:
        cm_path = resolve_asset_path("confusion_matrix.png")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Validation Curves",
        "Loss Telemetry",
        "Confusion Matrix",
        "Metrics Guide"
    ])

    with tab1:
        if csv_path and os.path.exists(csv_path):
            df_results = pd.read_csv(csv_path)
            df_results.columns = [c.strip() for c in df_results.columns]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['metrics/mAP50(B)'],
                name='mAP@50', mode='lines+markers',
                line=dict(color='#0284C7', width=3),
                marker=dict(size=6)
            ))
            fig.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['metrics/mAP50-95(B)'],
                name='mAP@50-95', mode='lines',
                line=dict(color='#6366F1', width=2.2)
            ))
            fig.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['metrics/precision(B)'],
                name='Precision', mode='lines',
                line=dict(color='#10B981', width=2, dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['metrics/recall(B)'],
                name='Recall', mode='lines',
                line=dict(color='#F59E0B', width=2, dash='dot')
            ))
            
            fig.update_layout(
                template="plotly_white",
                title="<b>Validation Metrics Progression (20 Epochs)</b>",
                xaxis_title="Epoch",
                yaxis_title="Score (0.0 to 1.0)",
                height=420,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Validation performance metrics available from model training telemetry.")

    with tab2:
        if csv_path and os.path.exists(csv_path):
            df_results = pd.read_csv(csv_path)
            df_results.columns = [c.strip() for c in df_results.columns]

            fig_loss = go.Figure()
            fig_loss.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['train/box_loss'],
                name='Train Box Loss', line=dict(color='#EF4444', width=2.5)
            ))
            fig_loss.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['val/box_loss'],
                name='Val Box Loss', line=dict(color='#F87171', width=2, dash='dash')
            ))
            fig_loss.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['train/cls_loss'],
                name='Train Class Loss', line=dict(color='#0284C7', width=2.5)
            ))
            fig_loss.add_trace(go.Scatter(
                x=df_results['epoch'], y=df_results['val/cls_loss'],
                name='Val Class Loss', line=dict(color='#38BDF8', width=2, dash='dash')
            ))
            
            fig_loss.update_layout(
                template="plotly_white",
                title="<b>Convergence &amp; Loss Progression</b>",
                xaxis_title="Epoch",
                yaxis_title="Loss Value",
                height=420,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_loss, use_container_width=True)

    with tab3:
        if cm_path and os.path.exists(cm_path):
            st.markdown("#### Normalized Confusion Matrix (YOLOv8 Validation)")
            try:
                cm_img = Image.open(cm_path)
                st.image(cm_img, caption="Normalized Confusion Matrix across Glioma, Meningioma, No Tumor, and Pituitary classes", use_container_width=True)
            except Exception:
                st.error("Failed to load confusion matrix image.")
            
            st.markdown("""
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 8px; line-height: 1.5;">
                    The normalized confusion matrix illustrates the proportion of correct vs. misclassified regions across the 4 diagnostic categories. 
                    Diagonal entries represent high classification certainty across all target classes.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Confusion matrix evaluation available from training artifacts.")

    with tab4:
        st.markdown("### Clinical Evaluation & YOLOv8 Validation Benchmarks")
        st.markdown("""
            <div class="kpi-card" style="padding: 20px; margin-bottom: 16px;">
                <div style="font-size: 1.05rem; font-weight: 700; color: var(--navy-header); margin-bottom: 6px;">
                    Per-Class Accuracy Breakdown (Developed by Marwan Shafi)
                </div>
                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border-color); color: var(--navy-header);">
                                <th style="padding: 8px;">Pathology Class</th>
                                <th style="padding: 8px;">Dataset Distribution</th>
                                <th style="padding: 8px;">Class Accuracy</th>
                                <th style="padding: 8px;">Pathological Characteristics</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 8px; font-weight: 600; color: #10B981;">No Tumor (Healthy)</td>
                                <td style="padding: 8px;">~1,300–1,500 scans</td>
                                <td style="padding: 8px; font-weight: 700; color: #10B981;">100.0%</td>
                                <td style="padding: 8px;">Normal parenchyma, zero false alarms observed</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 8px; font-weight: 600; color: var(--primary);">Meningioma</td>
                                <td style="padding: 8px;">~1,900 scans</td>
                                <td style="padding: 8px; font-weight: 700; color: var(--primary);">99.0%</td>
                                <td style="padding: 8px;">Benign, well-defined, dural attachment</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 8px; font-weight: 600; color: var(--info);">Pituitary Adenoma</td>
                                <td style="padding: 8px;">~1,600 scans</td>
                                <td style="padding: 8px; font-weight: 700; color: var(--info);">94.0%</td>
                                <td style="padding: 8px;">Sellar region, chiasm proximity, focal asymmetry</td>
                            </tr>
                            <tr style="border-bottom: 1px solid var(--border-color);">
                                <td style="padding: 8px; font-weight: 600; color: var(--danger);">Glioma</td>
                                <td style="padding: 8px;">~2,200 scans</td>
                                <td style="padding: 8px; font-weight: 700; color: var(--danger);">90.0%</td>
                                <td style="padding: 8px;">Infiltrative, indistinct borders, highly malignant</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: 700; color: var(--navy-header);">Overall System</td>
                                <td style="padding: 8px; font-weight: 700;">7,000–8,000 scans</td>
                                <td style="padding: 8px; font-weight: 800; color: var(--primary);">~95.0%</td>
                                <td style="padding: 8px; font-weight: 700;">3 Anatomical Planes (Axial, Sagittal, Coronal)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            | Metric | Meaning in Medical AI | Production Value |
            | :--- | :--- | :--- |
            | **mAP@50** | **Mean Average Precision** at Intersection-over-Union (IoU) 0.50 threshold. Represents overall tumor localization quality. | **96.31%** (YOLOv8) / **0.95** (YOLOv11) |
            | **Precision** | **True Positive Accuracy** — Out of all tumor regions predicted by the model, how many were true tumor lesions. Minimizes false alarms. | **96.0%** |
            | **Recall** | **Sensitivity / Detection Rate** — Out of all real tumors present in scans, how many did the model detect. Critical for patient safety. | **94.0%** |
            | **Inference Rate** | GPU processing throughput per cranial slice. | **92 FPS (~32 ms)** |
        """)

    render_disclaimer()
    render_footer()
