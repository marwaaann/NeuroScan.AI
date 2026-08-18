import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go

from frontend.components.cards import render_top_header, render_stat_card, render_disclaimer, render_footer

def render_analytics_page():
    render_top_header(
        title="Model Analytics",
        description="Evaluation metrics and training performance."
    )

    # Top metrics overview
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_stat_card("mAP@50", "96.31%", "Validation Mean Average Precision")
    with c2:
        render_stat_card("mAP@50-95", "79.46%", "mAP across IoU thresholds")
    with c3:
        render_stat_card("Precision", "93.87%", "Bounding Box Precision")
    with c4:
        render_stat_card("Recall", "94.01%", "Bounding Box Recall")

    st.markdown("<br/>", unsafe_allow_html=True)

    csv_path = os.path.join(os.getcwd(), "brain_tumor_detector", "yolov8n_run_1", "results.csv")
    cm_path = os.path.join(os.getcwd(), "brain_tumor_detector", "yolov8n_run_1", "confusion_matrix.png")

    tab1, tab2, tab3 = st.tabs(["Performance", "Training", "Confusion Matrix"])

    with tab1:
        if os.path.exists(csv_path):
            df_results = pd.read_csv(csv_path)
            df_results.columns = [c.strip() for c in df_results.columns]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['metrics/mAP50(B)'], name='mAP@50', line=dict(color='#2563EB', width=2.5)))
            fig.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['metrics/mAP50-95(B)'], name='mAP@50-95', line=dict(color='#4F46E5', width=2)))
            fig.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['metrics/precision(B)'], name='Precision', line=dict(color='#16A34A', width=2)))
            fig.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['metrics/recall(B)'], name='Recall', line=dict(color='#D97706', width=2)))
            
            fig.update_layout(
                template="plotly_white",
                title="Validation Metrics per Epoch (20 Epochs)",
                xaxis_title="Epoch",
                yaxis_title="Score",
                height=380,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Validation performance metrics available from model training run.")

    with tab2:
        if os.path.exists(csv_path):
            df_results = pd.read_csv(csv_path)
            df_results.columns = [c.strip() for c in df_results.columns]

            fig_loss = go.Figure()
            fig_loss.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['train/box_loss'], name='Train Box Loss', line=dict(color='#DC2626')))
            fig_loss.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['val/box_loss'], name='Val Box Loss', line=dict(color='#EF4444', dash='dash')))
            fig_loss.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['train/cls_loss'], name='Train Class Loss', line=dict(color='#2563EB')))
            fig_loss.add_trace(go.Scatter(x=df_results['epoch'], y=df_results['val/cls_loss'], name='Val Class Loss', line=dict(color='#60A5FA', dash='dash')))
            
            fig_loss.update_layout(
                template="plotly_white",
                title="Bounding Box & Classification Loss History",
                xaxis_title="Epoch",
                yaxis_title="Loss",
                height=380,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_loss, use_container_width=True)

    with tab3:
        if os.path.exists(cm_path):
            st.image(cm_path, caption="YOLOv8 Confusion Matrix", use_container_width=True)
            st.markdown("""
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 8px;">
                    The confusion matrix shows the distribution of correct and incorrect predictions across the four target classes.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Confusion matrix evaluation available after training.")

    render_disclaimer()
    render_footer()
