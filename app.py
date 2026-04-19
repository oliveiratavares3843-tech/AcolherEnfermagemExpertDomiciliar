import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from fpdf import FPDF

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Home Care Pro 2026", layout="wide")

# --- SISTEMA DE LOGIN ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if not st.session_state.auth:
        with st.container():
            st.subheader("🔒 Acesso Restrito - Equipe de Enfermagem")
            with st.form("Login"):
                user = st.text_input("Usuário")
                password = st.text_input("Senha", type="password")
                if st.form_submit_button("Entrar"):
                    # Usuário e senha padrão (Você pode alterar aqui)
                    if user == "enfermagem" and password == "2026":
                        st.session_state.auth = True
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos")
        return False
    return True

# --- FUNÇÕES DO BANCO DE DADOS (SQLite) ---
def init_db():
    conn = sqlite3.connect('homecare_2026.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS prontuario 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  data TEXT, 
                  paciente TEXT, 
                  enfermeira TEXT, 
                  pa TEXT, 
                  sat INT, 
                  dor TEXT, 
                  curativo TEXT, 
                  evolucao TEXT)''')
    conn.close()

# --- FUNÇÃO DE GERAÇÃO DE PDF (Corrigida para fpdf2) ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, txt="Relatorio de Atendimento Domiciliar", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=12)
    for chave, valor in dados.items():
        # Usamos multi_cell para que textos longos (como a evolução) quebrem linha sozinhos
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, txt=f"{chave}:", ln=True)
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, txt=str(valor))
        pdf.ln(2)
        
    return bytes(pdf.output())

# --- INTERFACE PRINCIPAL ---
if check_password():
    init_db()
    st.title("🩺 Gestão de Enfermagem Especializada")
    
    menu = st.sidebar.radio("Navegação", ["Novo Registro", "Histórico e Relatórios"])

    if menu == "Novo Registro":
        st.subheader("📝 Registrar Nova Visita")
        with st.form("visita", clear_on_submit=True):
            col1, col2 = st.columns(2)
            paciente = col1.text_input("Nome do Paciente")
            enfermeira = col2.text_input("Enfermeira Responsável")
            
            col3, col4, col5 = st.columns(3)
            pa = col3.text_input("Pressão Arterial (ex: 12/8)")
            sat = col4.number_input("Saturação O2 (%)", 0, 100, 95)
            dor = col5.selectbox("Escala de Dor", ["Sem dor", "Leve", "Moderada", "Intensa"])
            
            curativo = st.radio("Realizado Curativo?", ["Não", "Sim - Simples", "Sim - Complexo"])
            evolucao = st.text_area("Evolução Clínica Detalhada")
            
            if st.form_submit_button("Salvar Registro"):
                if paciente and enfermeira:
                    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
                    conn = sqlite3.connect('homecare_2026.db')
                    conn.execute("""INSERT INTO prontuario 
                                 (data, paciente, enfermeira, pa, sat, dor, curativo, evolucao) 
                                 VALUES (?,?,?,?,?,?,?,?)""",
                                 (data_atual, paciente, enfermeira, pa, sat, dor, curativo, evolucao))
                    conn.commit()
                    conn.close()
                    st.success("✅ Atendimento registrado com sucesso!")
                else:
                    st.warning("⚠️ Por favor, preencha o nome do paciente e da enfermeira.")

    elif menu == "Histórico e Relatórios":
        st.subheader("📋 Histórico de Atendimentos")
        conn = sqlite3.connect('homecare_2026.db')
        df = pd.read_sql_query("SELECT * FROM prontuario ORDER BY id DESC", conn)
        conn.close()

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            st.divider()
            st.subheader("📥 Gerar PDF para a Família")
            # Seleção do ID para gerar o relatório
            id_lista = df['id'].tolist()
            id_sel = st.selectbox("Selecione o ID do atendimento para gerar o PDF", id_lista)
            
            if st.button("Preparar PDF"):
                # Filtrar os dados da linha selecionada
                dados_linha = df[df['id'] == id_sel].iloc[0]
                
                pdf_data = {
                    "Data e Hora": dados_linha['data'],
                    "Paciente": dados_linha['paciente'],
                    "Enfermeira": dados_linha['enfermeira'],
                    "Pressão Arterial": dados_linha['pa'],
                    "Saturação": f"{dados_linha['sat']}%",
                    "Avaliação de Dor": dados_linha['dor'],
                    "Procedimento de Curativo": dados_linha['curativo'],
                    "Evolução Clínica": dados_linha['evolucao']
                }
                
                try:
                    pdf_bytes = gerar_pdf(pdf_data)
                    st.download_button(
                        label="⬇️ Baixar Relatório em PDF",
                        data=pdf_bytes,
                        file_name=f"Relatorio_{dados_linha['paciente']}_{dados_linha['id']}.pdf",
                        mime="application/pdf"
                    )
                    st.success("PDF gerado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao gerar o PDF: {e}")
        else:
            st.info("Nenhum registro encontrado.")
