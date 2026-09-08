import streamlit as st
from frontend.components.cards import render_top_header, render_disclaimer, render_footer
from frontend.components.icons import get_svg_icon

def render_about_page():
    """
    Render About NeuroScan.AI page with creator attribution,
    clinical dataset methodology, and technical deep learning architecture.
    """
    render_top_header(
        title="About NeuroScan.AI & Research Background",
        description="Clinical deep learning initiative for real-time brain MRI tumor localization and classification.",
        meta_text="Developed by Marwan Shafi • YOLOv8 & YOLOv11 Benchmarks • Multi-Planar MRI Analysis",
        badges=["AI Healthcare Innovation", "Deep Learning Vision", "Multi-Planar MRI", "Open-Source AI"]
    )

    col1, col2 = st.columns([1.6, 1.2], gap="large")

    with col1:
        st.markdown(f"### <span style='display:inline-flex; align-items:center; gap:8px;'>{get_svg_icon('paper', size=22, color='var(--primary)')} Research Paper Publication</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="kpi-card" style="padding: 24px; margin-bottom: 20px;">
                <div style="font-size: 1.18rem; font-weight: 800; color: var(--navy-header); margin-bottom: 8px;">
                    "Brain Tumor Detection Using YOLOv8 and YOLOv11"
                </div>
                <div style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 14px;">
                    Clinical Machine Learning &amp; Computer Vision Research Initiative.
                </div>
                <div style="font-size: 0.92rem; color: var(--text-secondary); line-height: 1.65; margin-bottom: 14px;">
                    <strong>Abstract &amp; Clinical Context:</strong> Brain tumor diagnosis through manual MRI reading is laborious, time-consuming, 
                    and vulnerable to inter-observer variability. Traditional CNN approaches (VGG16, ResNet) performed only slice-level classification 
                    without bounding-box localization. 
                    <br/><br/>
                    This research demonstrates automated, simultaneous lesion localization and multi-class diagnosis across 
                    <strong>Glioma</strong>, <strong>Meningioma</strong>, <strong>Pituitary</strong>, and <strong>No Tumor</strong> 
                    using state-of-the-art single-stage YOLO detectors. Experiments establish that modern YOLO architectures achieve 
                    <strong>0.95 mAP</strong> at <strong>92 FPS</strong> real-time inference rate.
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    <span class="tech-badge" style="background: rgba(0, 168, 150, 0.12); color: #007E70;">95% System Accuracy</span>
                    <span class="tech-badge" style="background: rgba(2, 132, 199, 0.12); color: #0284C7;">92 FPS Real-Time</span>
                    <span class="tech-badge" style="background: rgba(16, 185, 129, 0.12); color: #059669;">96% Precision</span>
                    <span class="tech-badge" style="background: rgba(99, 102, 241, 0.12); color: #4F46E5;">94% Recall</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### <span style='display:inline-flex; align-items:center; gap:8px;'>{get_svg_icon('sensitivity', size=22, color='var(--primary)')} Multi-Planar Dataset &amp; Methodology</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="kpi-card" style="padding: 24px; margin-bottom: 20px;">
                <div style="font-size: 0.92rem; color: var(--text-secondary); line-height: 1.65;">
                    The model was developed on a comprehensive cohort of <strong>7,000 to 8,000 cranial MRI scans</strong>:
                    <ul style="margin-top: 8px; margin-bottom: 12px; padding-left: 20px;">
                        <li><strong>Glioma:</strong> ~2,200 scans (irregular, indistinct borders, highly malignant glial neoplasms) — 90% accuracy</li>
                        <li><strong>Meningioma:</strong> ~1,900 scans (benign, well-circumscribed dural neoplasms) — 99% accuracy</li>
                        <li><strong>Pituitary:</strong> ~1,600 scans (sellar region neoplasms with chiasm proximity) — 94% accuracy</li>
                        <li><strong>No Tumor:</strong> ~1,300–1,500 scans (healthy tissue, zero false alarms) — 100% accuracy</li>
                    </ul>
                    <strong>Data Pipeline:</strong> Multi-perspective coverage across <em>axial</em>, <em>sagittal</em>, and <em>coronal</em> planes. 
                    Images standardized to 640×640 RGB, intensity normalized [0, 1], and augmented with ±15° rotations, spatial flips, Gaussian blur, 
                    and minority class balancing. 80% train / 20% validation split.
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### <span style='display:inline-flex; align-items:center; gap:8px;'>{get_svg_icon('precision', size=22, color='var(--primary)')} Future Research Directions</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="kpi-card" style="padding: 24px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 0.86rem; color: var(--text-secondary);">
                    <div>
                        <strong>1. 3D Volume Detection:</strong><br/>
                        Voxel-based 3D YOLO and vision transformers for volumetric volumetric MRI scans.
                    </div>
                    <div>
                        <strong>2. Multi-Modal Fusion:</strong><br/>
                        Simultaneous co-registration of T1-weighted, T2-weighted, and FLAIR sequences.
                    </div>
                    <div>
                        <strong>3. Explainable AI:</strong><br/>
                        Grad-CAM saliency mapping and attention heatmaps for clinical validation.
                    </div>
                    <div>
                        <strong>4. Hospital PACS Integration:</strong><br/>
                        DICOM ingestion and HL7/FHIR compatibility for radiology workflow integration.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"### <span style='display:inline-flex; align-items:center; gap:8px;'>{get_svg_icon('users', size=22, color='var(--primary)')} Project Creator &amp; Architect</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="kpi-card" style="padding: 24px; margin-bottom: 20px;">
                <div style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6;">
                    <div style="margin-bottom: 12px;">
                        <strong style="color: var(--navy-header); font-size: 1.08rem;">Marwan Shafi</strong><br/>
                        <span style="font-size: 0.84rem; color: var(--primary); font-weight: 600;">Lead Developer &amp; AI Architect</span>
                    </div>
                    <div style="font-size: 0.86rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 14px;">
                        Creator and lead builder of <strong>NeuroScan.AI</strong>. Designed and implemented the complete medical computer vision system, 
                        custom YOLOv8 inference pipeline, interactive clinical UI/UX design system, in-process latency optimizations, 
                        and production cloud deployment architecture.
                    </div>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                        <span class="tech-badge" style="background: rgba(0, 168, 150, 0.12); color: #007E70;">Lead Creator</span>
                        <span class="tech-badge" style="background: rgba(2, 132, 199, 0.12); color: #0284C7;">PyTorch &amp; YOLOv8</span>
                        <span class="tech-badge" style="background: rgba(16, 185, 129, 0.12); color: #059669;">Full-Stack AI Architecture</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### <span style='display:inline-flex; align-items:center; gap:8px;'>{get_svg_icon('link', size=22, color='var(--primary)')} Project &amp; Deployment Links</span>", unsafe_allow_html=True)
        st.markdown("""
            <div class="kpi-card" style="padding: 24px; margin-bottom: 20px;">
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <a href="https://github.com/marwaaann/NeuroScan.AI" target="_blank" style="text-decoration: none;">
                        <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: var(--primary);">
                            GitHub Repository (marwaaann/NeuroScan.AI) ➔
                        </div>
                    </a>
                    <a href="https://neuroscan-ai-lp16.onrender.com" target="_blank" style="text-decoration: none;">
                        <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: var(--navy-header);">
                            Primary Cloud Deployment (Render) ➔
                        </div>
                    </a>
                    <a href="https://neuroscanai-ahwmpetaryjhq9pm3qv4et.streamlit.app" target="_blank" style="text-decoration: none;">
                        <div style="background: var(--surface-elevated); border: 1px solid var(--border-color); padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: var(--navy-header);">
                            Streamlit Cloud App ➔
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### <span style='display:inline-flex; align-items:center; gap:8px;'>{get_svg_icon('stethoscope', size=22, color='var(--primary)')} Clinical Consultation</span>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="kpi-card" style="padding: 20px; text-align: center;">
                <div style="margin-bottom: 10px;">
                    {get_svg_icon('stethoscope', size=32, color='var(--primary)')}
                </div>
                <div style="font-weight: 700; color: var(--navy-header); margin-bottom: 6px;">
                    Schedule a Consultation
                </div>
                <div style="font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 14px;">
                    Explore multi-center hospital pilot integration or discuss research datasets.
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Tell Us How We Can Help ➔", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Contact Us"
            st.rerun()

    render_disclaimer()
    render_footer()

