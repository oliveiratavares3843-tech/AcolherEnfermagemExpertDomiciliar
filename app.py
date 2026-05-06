import streamlit as st
from fpdf import FPDF

# Configuração da página do Streamlit
st.set_page_config(page_title="Gestão de Enfermagem", layout="centered")

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Relatório de Atendimento de Enfermagem", ln=True, align='C')
    pdf.ln(10) # Espaço
    
    # Dados do Paciente e Enfermeiro
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Paciente: {dados['paciente']}", ln=True)
    pdf.cell(0, 10, txt=f"Enfermeiro(a) Responsável: {dados['enfermeiro']}", ln=True)
    
    # Sinais Vitais em uma linha
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    sinais = f"PA: {dados['pa']}  |  Saturação: {dados['saturacao']}%  |  Escala de Dor: {dados['dor']}"
    pdf.cell(0, 10, txt=sinais, ln=True, border=1)
    
    # Evolução Clínica (Onde o multi_cell é essencial)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Evolução Clínica Detalhada:", ln=True)
    
    pdf.set_font("Arial", '', 12)
    # multi_cell(largura, altura_da_linha, texto, borda, alinhamento)
    # w=0 faz ocupar a largura total da página
    pdf.multi_cell(w=0, h=8, txt=dados['evolucao'], border=0, align='J')
    
    return pdf.output(dest='S').encode('latin-1')

# Interface do App
st.title("🩺 Gestão de Enfermagem Especializada")
st.subheader("Registrar Nova Visita")

col1, col2 = st.columns(2)
with col1:
    nome_paciente = st.text_input("Nome do Paciente")
    pa = st.text_input("Pressão Arterial (ex: 12/8)")
with col2:
    enfermeiro = st.text_input("Enfermeira Responsável")
    saturacao = st.number_input("Saturação O2 (%)", min_value=0, max_value=100, value=95)

dor = st.selectbox("Escala de Dor", ["Sem dor", "Dor Leve", "Dor Moderada", "Dor Intensa"])
evolucao_texto = st.text_area("Evolução Clínica Detalhada", height=200)

if st.button("Gerar Relatório PDF"):
    if nome_paciente and evolucao_texto:
        dados_visita = {
            "paciente": nome_paciente,
            "enfermeiro": enfermeiro,
            "pa": pa,
            "saturacao": saturacao,
            "dor": dor,
            "evolucao": evolucao_texto
        }
        
        pdf_bytes = gerar_pdf(dados_visita)
        
        st.success("PDF gerado com sucesso!")
        st.download_button(
            label="Clique aqui para baixar o PDF",
            data=pdf_bytes,
            file_name=f"evolucao_{nome_paciente}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Por favor, preencha o nome do paciente e a evolução clínica.")

