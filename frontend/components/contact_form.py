import streamlit as st
import re
from frontend.services.api_client import get_api_client

def render_contact_form(compact: bool = False):
    """
    Renders the NURA-inspired 'Tell us how we can help' contact & consultation form,
    matching the layout and fields in the reference design.
    Submissions are stored directly in the backend SQLite database.
    """
    st.markdown("""
        <div class="nura-contact-card">
            <div class="nura-contact-header">
                <div class="nura-contact-title">Tell us how we can help</div>
                <div class="nura-contact-subtitle">
                    Schedule an AI screening demonstration, request research data, or partner on multi-center MRI clinical validation.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        c_form = st.form(key="nura_contact_inquiry_form", clear_on_submit=False)
        with c_form:
            c1, c2 = st.columns([1, 1])
            with c1:
                full_name = st.text_input(
                    "Full Name *",
                    placeholder="Full Name",
                    help="Enter your complete legal or professional name"
                )
            with c2:
                email = st.text_input(
                    "Email address (optional)",
                    placeholder="Email address (optional)",
                    help="Your email address for receiving verification reports"
                )

            c3, c4 = st.columns([1, 1])
            with c3:
                phone = st.text_input(
                    "+91 Phone Number *",
                    placeholder="+91 Phone Number",
                    help="Enter your 10-digit mobile number with +91 country code"
                )
            with c4:
                location = st.selectbox(
                    "Select Location *",
                    [
                        "Select Location",
                        "Bengaluru",
                        "Delhi NCR (New Delhi / Gurugram / Noida)",
                        "Mumbai",
                        "Hyderabad",
                        "Chennai",
                        "Kolkata",
                        "Pune",
                        "Ahmedabad",
                        "Other (India)",
                        "International / Overseas"
                    ],
                    index=0,
                    help="Primary clinical facility or city location"
                )

            inquiry_notes = st.text_area(
                "Clinical Notes or Specific Inquiry (optional)",
                placeholder="Share any specific scanning protocol, MRI plane, or research collaboration questions...",
                height=70
            )

            terms_agreed = st.checkbox(
                "I agree to the privacy policy, terms & conditions, and clinical research communications.",
                value=True
            )

            submit_btn = st.form_submit_button("Submit Request ➔", type="primary", use_container_width=True)

        if submit_btn:
            # Client-side validation
            clean_name = full_name.strip() if full_name else ""
            clean_phone = phone.strip() if phone else ""
            
            # Basic validation
            errors = []
            if not clean_name or len(clean_name) < 2:
                errors.append("Please enter your Full Name.")
            
            # Extract digits from phone
            digits = re.sub(r"[^\d]", "", clean_phone)
            if len(digits) < 10:
                errors.append("Please provide a valid 10-digit phone number.")

            if location == "Select Location":
                errors.append("Please select a location.")

            if not terms_agreed:
                errors.append("Please agree to the privacy policy and terms to proceed.")

            if errors:
                for err in errors:
                    st.error(f"⚠️ {err}")
            else:
                with st.spinner("Submitting your inquiry to NeuroScan.AI backend..."):
                    client = get_api_client()
                    success, res = client.submit_contact(
                        full_name=clean_name,
                        phone=clean_phone,
                        location=location,
                        email=email.strip() if email else "",
                        message=inquiry_notes.strip() if inquiry_notes else ""
                    )

                    if success:
                        contact_id = res.get("contact_id", "REF-#" + digits[-4:])
                        st.success(f"""
                            **Inquiry Submitted Successfully! (Reference ID: #{contact_id})**  
                            Thank you, **{clean_name}**. Your consultation request has been securely stored in the NeuroScan.AI database.  
                            Our clinical specialist team ({location}) will review your request and reach out at `{clean_phone}` shortly.
                        """)
                    else:
                        st.error(f"Submission failed: {res.get('error', 'Unknown backend error')}")
