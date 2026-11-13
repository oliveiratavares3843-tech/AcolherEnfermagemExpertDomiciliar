# 🩺 Home Care Nursing System

![Python](https://shields.io)
![Streamlit](https://shields.io)
![FPDF](https://shields.io)
![Pillow](https://shields.io)

A specialized clinical management and automated medical reporting web application built with **Python**, **Streamlit**, **FPDF**, and **Pillow**. Tailored for home care nursing professionals to record patient vitals, document clinical evolutions, and export branded PDF reports.

🔗 **Live Demo:** **[Access the Clinical Portal](https://sistema-enfermagem.streamlit.app/)**

---

## 🔐 Demo Credentials (For Recruiters & Evaluators)

Use the credentials below to access the clinical portal and test PDF report generation:

* **Username:** `recruiter`
* **Password:** `nurse2026`

---

## ✨ Key Features

* **Context-Aware UI Styling:** Custom healthcare-themed gradient interface on the Welcome and Login screens that transitions to a clean, high-contrast clinical workspace upon authentication.
* **Vital Signs & Clinical Tracking:** Structured capture of Blood Pressure (BP), Oxygen Saturation (SpO2), Pain Scale levels, and detailed nursing notes.
* **Automated PDF Report Generation:** Dynamically compiles patient data, vitals, clinical notes, and custom company logos into downloadable A4 PDF documents.
* **Character Encoding Resilience:** Built-in `latin-1` fallback handling to prevent PDF rendering failures with special characters.

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **Framework:** Streamlit
* **PDF Engine:** FPDF
* **Image Processing:** Pillow (PIL)

---

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd AcolherEnfermagemExpertDomiciliar
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```
