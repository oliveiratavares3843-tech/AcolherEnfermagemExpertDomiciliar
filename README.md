# Acimport streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Home Care 2026", layout="wide")

# Função para conectar ao banco de dados (SQLite)
def conectar_bd():
    conn = sqlite3.connect('atendimentos_v2026.db')
    return conn

# Criar a tabela se não existir
conn = conectar_bd()
conn.execute('''CREATE TABLE IF NOT EXISTS prontuario 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              data TEXT, paciente TEXT, enfermeira TEXT, 
              pa TEXT, sat INTEGER, temp TEXT, evolucao TEXT)''')
conn.close()

st.title("🩺 Sistema de Gestão - Enfermagem Especializada")
st.sidebar.header("Menu de Navegação")
aba = st.sidebar.radio("Ir para:", ["Registrar Visita", "Histórico de Pacientes"])

if aba == "Registrar Visita":
    st.subheader("📝 Novo Registro de Evolução Clínica")
    
    with st.form("form_visita", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            paciente = st.text_input("Nome do Paciente")
            enfermeira = st.text_input("Enfermeira Responsável")
        with col2:
            data_visita = st.date_input("Data da Visita", datetime.now())
            pa = st.text_input("Pressão Arterial (ex: 120/80)")

        col3, col4 = st.columns(2)
        with col3:
            sat = st.number_input("Saturação O2 (%)", min_value=0, max_value=100, value=95)
        with col4:
            temp = st.text_input("Temperatura (ex: 36.5°C)")
            
        evolucao = st.text_area("Evolução de Enfermagem (Detalhada)")
        
        botao_salvar = st.form_submit_button("Salvar no Prontuário")

    if botao_salvar:
        conn = conectar_bd()
        conn.execute('''INSERT INTO prontuario (data, paciente, enfermeira, pa, sat, temp, evolucao) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                     (data_visita.strftime("%d/%m/%Y"), paciente, enfermeira, pa, sat, temp, evolucao))
        conn.commit()
        conn.close()
        st.success("✅ Registro salvo com sucesso e sincronizado!")

elif aba == "Histórico de Pacientes":
    st.subheader("📋 Consultar Prontuários")
    
    conn = conectar_bd()
    df = pd.read_sql_query("SELECT * FROM prontuario ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        # Filtro simples por paciente
        busca = st.text_input("Buscar por nome do paciente")
        if busca:
            df = df[df['paciente'].str.contains(busca, case=False)]
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum atendimento registrado até o momento.")
olherEnfermagemExpertDomiciliar
