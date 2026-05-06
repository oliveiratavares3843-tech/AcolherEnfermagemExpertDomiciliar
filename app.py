import streamlit as st
from fpdf import FPDF

# --- 1. CONFIGURAÇÃO DE SEGURANÇA (LOGIN) ---
USUARIO_SISTEMA = "acolher"
SENHA_SISTEMA = "enfermagem2027"

def sistema_login():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if not st.session_state.logado:
        st.markdown("<h2 style='text-align: center;'>🔐 Acesso ao Sistema</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                if usuario == USUARIO_SISTEMA and senha == SENHA_SISTEMA:
                    st.session_state.logado = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
        return False
    return True

# --- 2. FUNÇÃO PARA GERAR O PDF (CORREÇÃO DEFINITIVA) ---
def gerar_pdf(dados):
    # Usamos o FPDF padrão
    pdf = FPDF()
    pdf.add_page()
    
    # Tentativa de colocar o logotipo
    try:
        pdf.image("logo.png", 10, 8, 33) 
    except:
        pass 

    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.ln(20) 
    pdf.cell(0, 10, txt="Relatório de Atendimento Domiciliar", ln=True, align='C')
    pdf.ln(10)
    
    # Dados do Paciente e Enfermeiro
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Paciente: {dados['paciente']}", ln=True)
    pdf.cell(0, 10, txt=f"Enfermeiro(a): {dados['enfermeiro']}", ln=True)
    
    # Sinais Vitais
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    sinais = f"PA: {dados['pa']} | SatO2: {dados['saturacao']}% | Dor: {dados['dor']}"
    pdf.cell(0, 10, txt=sinais, ln=True, border=1, align='C')
    
    # Evolução Clínica (Quebra de linha automática)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Evolução Clínica Detalhada:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(w=0, h=8, txt=dados['evolucao'], border=0, align='J')
    
    # AJUSTE AQUI: Convertendo bytearray para bytes explicitamente
    return bytes(pdf.output())

# --- 3. INTERFACE DO APLICATIVO ---
if sistema_login():
    st.sidebar.title("Menu")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    st.title("🩺 Gestão de Enfermagem Especializada")
    st.write("---")
    st.subheader("Registrar Nova Visita")

    col1, col2 = st.columns(2)
    with col1:
        nome_paciente = st.text_input("Nome do Paciente")
        pa = st.text_input("Pressão Arterial (ex: 12/8)")
    with col2:
        enfermeiro = st.text_input("Enfermeira Responsável")
        saturacao = st.number_input("Saturação O2 (%)", 0, 100, 95)

    dor = st.selectbox("Escala de Dor", ["Sem dor", "Leve", "Moderada", "Intensa"])
    evolucao_texto = st.text_area("Evolução Clínica Detalhada", height=200)

    if st.button("Gerar Relatório PDF"):
        if nome_paciente and evolucao_texto:
            try:
                dados_visita = {
                    "paciente": nome_paciente, 
                    "enfermeiro": enfermeiro,
                    "pa": pa, 
                    "saturacao": saturacao, 
                    "dor": dor, 
                    "evolucao": evolucao_texto
                }
                
                # O pdf_output agora virá como bytes puros
                pdf_bytes = gerar_pdf(dados_visita)
                
                st.success("✅ Relatório gerado com sucesso!")
                
                st.download_button(
                    label="📥 Baixar Documento PDF",
                    data=pdf_bytes,
                    file_name=f"atendimento_{nome_paciente}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao processar PDF: {e}")
        else:
            st.warning("⚠️ Preencha os campos obrigatórios.")

