import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from fpdf import FPDF

# --- CONFIGURAÇÃO E LOGIN ---
st.set_page_config(page_title="Home Care Pro 2026", layout="wide")

def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        with st.form("Login"):
            st.subheader("🔒 Acesso Restrito")
            user = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                if user == "enfermagem" and password == "2026": # Mude sua senha aqui!
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
        return False
    return True

# --- FUNÇÕES DE BANCO DE DATA ---
def init_db():
    conn = sqlite3.connect('homecare_2026.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS prontuario 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, paciente TEXT, 
                  enfermeira TEXT, pa TEXT, sat INT, dor TEXT, curativo TEXT, evolucao TEXT)''')
    conn.close()

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Relatorio de Atendimento Domiciliar", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    for chave, valor in dados.items():
        pdf.cell(200, 10, f"{chave}: {valor}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE PRINCIPAL ---
if check_password():
    init_db()
    st.title("🩺 Gestão de Enfermagem Especializada")
    
    menu = st.sidebar.radio("Navegação", ["Novo Registro", "Histórico e Relatórios"])

    if menu == "Novo Registro":
        with st.form("visita"):
            col1, col2 = st.columns(2)
            paciente = col1.text_input("Nome do Paciente")
            enfermeira = col2.text_input("Enfermeira Responsável")
            
            col3, col4, col5 = st.columns(3)
            pa = col3.text_input("Pressão Arterial")
            sat = col4.number_input("Saturação O2 (%)", 0, 100, 95)
            dor = col5.selectbox("Escala de Dor", ["Sem dor", "Leve", "Moderada", "Intensa"])
            
            curativo = st.radio("Realizado Curativo?", ["Não", "Sim - Simples", "Sim - Complexo"])
            evolucao = st.text_area("Evolução Clínica Detalhada")
            
            if st.form_submit_button("Salvar Registro"):
                data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
                conn = sqlite3.connect('homecare_2026.db')
                conn.execute("INSERT INTO prontuario (data, paciente, enfermeira, pa, sat, dor, curativo, evolucao) VALUES (?,?,?,?,?,?,?,?)",
                             (data_atual, paciente, enfermeira, pa, sat, dor, curativo, evolucao))
                conn.commit()
                conn.close()
                st.success("Dados salvos com sucesso!")

    elif menu == "Histórico e Relatórios":
        conn = sqlite3.connect('homecare_2026.db')
        df = pd.read_sql_query("SELECT * FROM prontuario ORDER BY id DESC", conn)
        conn.close()

        if not df.empty:
            st.dataframe(df)
            
            st.subheader("📥 Gerar Relatório para Família")
            id_sel = st.selectbox("Selecione o ID do atendimento", df['id'])
            if st.button("Preparar PDF"):
                row = df[df['id'] == id_sel].iloc[0]
                pdf_data = {
                    "Data": row['data'], "Paciente": row['paciente'], 
                    "Enfermeira": row['enfermeira'], "Sinais Vitais": f"PA: {row['pa']} | Sat: {row['sat']}%",
                    "Avaliação de Dor": row['dor'], "Procedimento": row['curativo'],
                    "Evolução": row['evolucao']
                }
                pdf_output = gerar_pdf(pdf_data)
                st.download_button(label="Baixar PDF do Atendimento", data=pdf_output, 
                                 file_name=f"Relatorio_{row['paciente']}.pdf", mime="application/pdf")


