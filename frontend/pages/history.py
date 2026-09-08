import streamlit as st
import io
from PIL import Image
from frontend.components.cards import render_top_header, render_disclaimer, render_footer

def render_history_page():
    """Render Session Scan History page showing all scans evaluated in the current session"""
    render_top_header(
        title="Session Scan History",
        description="Review all MRI scans analyzed during your active clinical research session.",
        meta_text="Session Scans Log • Local In-Memory Storage",
        badges=["Audit Trail", "Session Log", "Re-Inspect"]
    )

    history = st.session_state.get("scan_history", [])

    if not history:
        st.markdown("""
            <div class="kpi-card" style="text-align: center; padding: 60px 24px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">📁</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">
                    No History Recorded Yet
                </div>
                <div style="font-size: 0.92rem; color: var(--text-secondary); max-width: 440px; margin: 0 auto; line-height: 1.5;">
                    Scans analyzed during your session will automatically be recorded here for clinical comparison and review.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Go to MRI Analysis ➔", type="primary"):
            st.session_state["current_page"] = "MRI Analysis"
            st.rerun()
    else:
        st.markdown(f"### Recent Evaluations ({len(history)} Scans)")
        
        for idx, item in enumerate(history):
            with st.container():
                c_img, c_info, c_action = st.columns([1, 3, 1.2], gap="medium")
                
                with c_img:
                    try:
                        thumb = Image.open(io.BytesIO(item["bytes"]))
                        st.image(thumb, use_container_width=True)
                    except Exception:
                        st.write("MRI Scan")

                with c_info:
                    st.markdown(f"#### `{item['filename']}`")
                    st.markdown(f"**Analyzed on:** `{item['timestamp']}`")
                    
                    if item["count"] > 0:
                        conf_pct = item["confidence"] * 100
                        st.markdown(f"""
                            <div style="margin-top: 6px;">
                                <span class="pill-status" style="background: rgba(239, 68, 68, 0.15); color: var(--danger);">
                                    🚨 {item['primary_class']} ({conf_pct:.1f}%)
                                </span>
                                <span style="font-size: 0.8rem; color: var(--text-muted); margin-left: 8px;">
                                    {item['count']} Region(s) Localized
                                </span>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <div style="margin-top: 6px;">
                                <span class="pill-status pill-online">
                                    ✅ No Lesion Detected
                                </span>
                            </div>
                        """, unsafe_allow_html=True)

                with c_action:
                    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
                    if st.button("View Full Result", key=f"view_hist_{item['id']}", use_container_width=True, type="secondary"):
                        st.session_state["last_pred"] = item["pred"]
                        st.session_state["last_bytes"] = item["bytes"]
                        st.session_state["last_filename"] = item["filename"]
                        st.session_state["current_page"] = "MRI Analysis"
                        st.rerun()

                st.markdown("---")

        if st.button("Clear Scan History", type="secondary"):
            st.session_state["scan_history"] = []
            st.rerun()

    render_disclaimer()
    render_footer()
