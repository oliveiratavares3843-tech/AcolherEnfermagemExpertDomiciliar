import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# --- 1. CONFIGURAÇÃO DE SEGURANÇA (LOGIN) ---
USUARIO_SISTEMA = "acolher"
SENHA_SISTEMA = "enfermagem2024"

def sistema_login():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if not st.session_state.logado:
        # --- O AZUL FICA SÓ AQUI DENTRO ---
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

        # Ícone de entrada (Emoji ou Imagem)
        st.markdown("<h1 style='text-align: center; font-size: 80px;'>🩺</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #005DAE;'>💙 Acesso ao Sistema</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                if usuario == USUARIO_SISTEMA and senha == SENHA_SISTEMA:
                    st.session_state.logado = True
                    st.rerun() # Ao recarregar logado, ele ignora o CSS acima
                else:
                    st.error("Usuário ou senha incorretos.")
        return False
    return True

# --- 2. FUNÇÃO PARA GERAR O PDF ---
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
        except: pass

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

# --- 3. INTERFACE DO APLICATIVO (TELA BRANCA APÓS LOGIN) ---
if sistema_login():
    # Aqui não tem CSS de fundo, então volta ao padrão (Branco/Cinza claro)
    st.sidebar.title("⚙️ Configurações")
    logo_carregada = st.sidebar.file_uploader("Logotipo da Empresa", type=["png", "jpg", "jpeg"])
    
    if st.sidebar.button("Sair do Sistema"):
        st.session_state.logado = False
        st.rerun()

    st.title("🩺 Gestão de Enfermagem")
    st.write("---")
    
    st.subheader("Registrar Nova Visita")
    col1, col2 = st.columns(2)
    with col1:
        nome_paciente = st.text_input("Nome do Paciente")
        pa = st.text_input("Pressão Arterial")
    with col2:
        enfermeiro = st.text_input("Enfermeira Responsável")
        saturacao = st.number_input("Saturação O2 (%)", 0, 100, 95)

    dor = st.selectbox("Escala de Dor", ["Sem dor", "Leve", "Moderada", "Intensa"])
    evolucao_texto = st.text_area("Evolução Clínica Detalhada", height=250)

    if st.button("Gerar Relatório PDF"):
        if nome_paciente and evolucao_texto:
            try:
                dados_visita = {
                    "paciente": nome_paciente, "enfermeiro": enfermeiro,
                    "pa": pa, "saturacao": f"{saturacao}", "dor": dor, "evolucao": evolucao_texto
                }
                pdf_bytes = gerar_pdf(dados_visita, logo_carregada)
                st.success("✅ Relatório gerado com sucesso!")
                st.download_button(
                    label="📥 Baixar PDF",
                    data=pdf_bytes,
                    file_name=f"atendimento_{nome_paciente}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao gerar: {e}")
        else:
            st.warning("⚠️ Preencha os campos obrigatórios.")

