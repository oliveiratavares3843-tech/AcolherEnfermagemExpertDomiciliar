import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# 1. ESTE DEVE SER O PRIMEIRO COMANDO STREAMLIT DO ARQUIVO
st.set_page_config(page_title="Acolher Enfermagem")

# 2. ESTILO GLOBAL (CSS) - APLICA O AZUL SO NA PRIMEIRA TELA 
st.markdown("""
    <style>
    /* Fundo azul degradê fixo */
    .stApp {
        background: linear-gradient(180deg, #A2D9FF 0%, #FFFFFF 100%) !important;
        background-attachment: fixed;
    }
    
    /* Botões em azul forte */
    .stButton > button {
        background-color: #005DAE !important;
        color: white !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        border: none !important;
    }

    /* Arredondamento das caixas de texto */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE SEGURANÇA ---
USUARIO_SISTEMA = "acolher"
SENHA_SISTEMA = "enfermagem2026"

def sistema_login():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if not st.session_state.logado:
        # Centralizando o ícone na entrada
        col_img1, col_img2, col_img3 = st.columns([1,1,1])
        with col_img2:
            st.image("https://flaticon.com", width=120)

        st.markdown("<h2 style='text-align: center; color: #005DAE;'>💙 Acesso ao Sistema</h2>", unsafe_allow_html=True)
        
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

# --- FUNÇÃO DO PDF ---
def gerar_pdf(dados, arquivo_logo):
    pdf = FPDF()
    pdf.add_page()
    if arquivo_logo is not None:
        try:
            img = Image.open(arquivo_logo)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            pdf.image(img_byte_arr, 10, 8, 33)
        except:
            pass

    pdf.set_font("Arial", 'B', 16)
    pdf.ln(25) 
    pdf.cell(0, 10, txt="Relatorio de Atendimento Domiciliar", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Paciente: {dados['paciente']}", ln=True)
    pdf.cell(0, 10, txt=f"Enfermeiro(a): {dados['enfermeiro']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    sinais = f"PA: {dados['pa']} | SatO2: {dados['saturacao']}% | Dor: {dados['dor']}"
    pdf.cell(0, 10, txt=sinais, ln=True, border=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Evolucao Clinica Detalhada:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(w=0, h=8, txt=dados['evolucao'], border=0, align='J')
    return bytes(pdf.output())

# --- INTERFACE PRINCIPAL (APÓS LOGIN) ---
if sistema_login():
    st.sidebar.markdown("### ⚙️ Painel de Controle")
    logo_carregada = st.sidebar.file_uploader("Logotipo da Empresa", type=["png", "jpg", "jpeg"])
    
    st.sidebar.write("---")
    if st.sidebar.button("Sair do Sistema"):
        st.session_state.logado = False
        st.rerun()

    st.title("🩺 Gestão de Enfermagem Especializada")
    st.write("---")
    
    st.subheader("📝 Registrar Nova Visita")

    col1, col2 = st.columns(2)
    with col1:
        nome_paciente = st.text_input("Nome do Paciente")
        pa = st.text_input("Pressão Arterial")
    with col2:
        enfermeiro = st.text_input("Enfermeira Responsável")
        saturacao = st.number_input("Saturação O2 (%)", 0, 100, 95)

    dor = st.selectbox("Escala de Dor", ["Sem dor", "Leve", "Moderada", "Intensa"])
    evolucao_texto = st.text_area("Evolução Clínica Detalhada", height=200)

    if st.button("🚀 Gerar Relatório"):
        if nome_paciente and evolucao_texto:
            try:
                dados_visita = {
                    "paciente": nome_paciente, "enfermeiro": enfermeiro,
                    "pa": pa, "saturacao": f"{saturacao}", "dor": dor, "evolucao": evolucao_texto
                }
                pdf_bytes = gerar_pdf(dados_visita, logo_carregada)
                st.success("✅ Relatório gerado!")
                st.download_button(
                    label="📥 Baixar PDF",
                    data=pdf_bytes,
                    file_name=f"atendimento_{nome_paciente}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.warning("⚠️ Preencha os campos obrigatórios.")

