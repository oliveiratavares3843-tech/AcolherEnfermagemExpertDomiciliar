import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Page configuration
st.set_page_config(page_title="Home Care Nursing System", page_icon="🩺", layout="centered")

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Demo credentials for recruiters + your original credentials
DEMO_USERS = {
    "recruiter": "nurse2026",
    "acolher": "enfermagem2026"
}

# Custom blue gradient style for Home and Login screens
def apply_welcome_style():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(180deg, #A2D9FF 0%, #FFFFFF 100%) !important;
        }
        .stButton > button {
            width: 100%;
            background-color: #005DAE !important;
            color: white !important;
            border-radius: 25px !important;
            font-weight: bold !important;
        }
        </style>
        """, unsafe_allow_html=True)

# --- 1. HOME SCREEN ---
def home_screen():
    apply_welcome_style()
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>🩺</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #005DAE;'>Home Care Nursing System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #333;'>Specialized clinical evolution management and automated PDF medical reporting.</p>", unsafe_allow_html=True)
    st.write("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Access Clinical Portal ➡️"):
            st.session_state.page = "login"
            st.rerun()

# --- 2. LOGIN SCREEN ---
def login_screen():
    apply_welcome_style()
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>🩺</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #005DAE;'>💙 System Access</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Visible demo credentials for recruiters
        st.info("👋 **Recruiter / Visitor Demo Access:**\n\n* **Username:** `recruiter`\n* **Password:** `nurse2026`")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            secrets_users = st.secrets.get("usuarios", {}) if hasattr(st, "secrets") else {}
            valid_users = {**DEMO_USERS, **secrets_users}

            if username in valid_users and str(valid_users[username]) == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.page = "system"
                st.rerun()
            else:
                st.error("⚠️ Invalid username or password.")
        
        if st.button("⬅️ Back to Home"):
            st.session_state.page = "home"
            st.rerun()

# --- 3. PDF GENERATOR FUNCTION ---
def generate_pdf(data, logo_file):
    pdf = FPDF()
    pdf.add_page()
    if logo_file is not None:
        try:
            img = Image.open(logo_file)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            pdf.image(img_byte_arr, 10, 8, 33)
        except Exception:
            pass

    pdf.set_font("Arial", 'B', 16)
    pdf.ln(25) 
    pdf.cell(0, 10, txt="Home Care Clinical Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Patient: {data['patient']}", ln=True)
    pdf.cell(0, 10, txt=f"Nurse in Charge: {data['nurse']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    vitals = f"BP: {data['bp']} | SpO2: {data['saturation']}% | Pain Level: {data['pain']}"
    pdf.cell(0, 10, txt=vitals, ln=True, border=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Detailed Clinical Evolution:", ln=True)
    pdf.set_font("Arial", '', 12)
    # Latin-1 encoding fallback to prevent FPDF crashes with special characters
    safe_evolution = data['evolution'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(w=0, h=8, txt=safe_evolution, border=0, align='J')
    return bytes(pdf.output())

# --- 4. MAIN APPLICATION INTERFACE (WHITE THEME AFTER LOGIN) ---
def system_screen():
    st.sidebar.header("👤 Active Session")
    st.sidebar.info(f"Logged in as: **{st.session_state.current_user}**")
    
    st.sidebar.title("⚙️ Settings")
    uploaded_logo = st.sidebar.file_uploader("Company Logo", type=["png", "jpg", "jpeg"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.rerun()

    st.title("🩺 Specialized Nursing Management")
    st.write("---")
    
    st.subheader("Register New Patient Visit")
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Patient Name")
        bp = st.text_input("Blood Pressure (e.g., 120/80)")
    with col2:
        nurse_name = st.text_input("Nurse in Charge")
        saturation = st.number_input("O2 Saturation (%)", 0, 100, 95)

    pain_level = st.selectbox("Pain Scale", ["No pain", "Mild", "Moderate", "Severe"])
    clinical_evolution = st.text_area("Detailed Clinical Evolution", height=250)

    if st.button("Generate PDF Report", type="primary"):
        if patient_name and clinical_evolution:
            try:
                visit_data = {
                    "patient": patient_name,
                    "nurse": nurse_name,
                    "bp": bp,
                    "saturation": f"{saturation}",
                    "pain": pain_level,
                    "evolution": clinical_evolution
                }
                pdf_bytes = generate_pdf(visit_data, uploaded_logo)
                st.success("✅ Report generated successfully!")
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"clinical_report_{patient_name.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
        else:
            st.warning("⚠️ Please fill in the required fields (Patient Name and Clinical Evolution).")

# --- ROUTING CONTROL ---
if st.session_state.page == "home":
    home_screen()
elif st.session_state.page == "login":
    login_screen()
elif st.session_state.page == "system":
    if st.session_state.logged_in:
        system_screen()
    else:
        st.session_state.page = "login"
        st.rerun()

