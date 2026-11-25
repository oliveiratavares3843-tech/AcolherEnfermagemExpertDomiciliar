import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Page configuration
st.set_page_config(page_title="Home Care Nursing System", page_icon="🩺", layout="centered")

# --- PDF GENERATOR FUNCTION ---
def generate_pdf(data, logo_file):
    pdf = FPDF()
    pdf.add_page()
    if logo_file is not None:
        try:
            img = Image.open(logo_file)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)
            pdf.image(img_byte_arr, 10, 8, 33)
        except Exception:
            pass

    pdf.set_font("Arial", "B", 16)
    pdf.ln(25)
    pdf.cell(0, 10, txt="Home Care Clinical Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt=f"Patient: {data['patient']}", ln=True)
    pdf.cell(0, 10, txt=f"Nurse in Charge: {data['nurse']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    vitals = f"BP: {data['bp']} | SpO2: {data['saturation']}% | Pain Level: {data['pain']}"
    pdf.cell(0, 10, txt=vitals, ln=True, border=1, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Detailed Clinical Evolution:", ln=True)
    pdf.set_font("Arial", "", 12)
    safe_evolution = data["evolution"].encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(w=0, h=8, txt=safe_evolution, border=0, align="J")
    return bytes(pdf.output())

# --- MAIN APPLICATION INTERFACE ---
def system_screen():
    st.sidebar.title("⚙️ Settings")
    uploaded_logo = st.sidebar.file_uploader("Company Logo", type=["png", "jpg", "jpeg"])

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
                    "evolution": clinical_evolution,
                }
                pdf_bytes = generate_pdf(visit_data, uploaded_logo)
                st.success("✅ Report generated successfully!")
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"clinical_report_{patient_name.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
        else:
            st.warning("⚠️ Please fill in the required fields (Patient Name and Clinical Evolution).")

if __name__ == "__main__":
    system_screen()


