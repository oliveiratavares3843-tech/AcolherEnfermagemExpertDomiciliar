import streamlit as st
from fpdf import FPDF

# --- CONFIGURAÇÃO DE LOGIN ---
# Defina aqui seu usuário e senha
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "enfermagem123"

def verificar_login():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔐 Acesso Restrito")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
        return False
    return True

# --- FUNÇÃO PARA GERAR PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Inserindo Logotipo (Verifica se o arquivo existe para não travar)
    try:
        # Altere "logo.png" para o nome real do seu arquivo no GitHub
        pdf.image("logo.png", 10, 8, 33) 
    except:
        pass # Se não achar a imagem, ignora e segue

    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.ln(20) 
    pdf.cell(0, 10, txt="Relatório de Atendimento de Enfermagem", ln=True, align='C')
    pdf.ln(10)
    
    # Dados Principais
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Paciente: {dados['paciente']}", ln=True)
    pdf.cell(0, 10, txt=f"Enfermeiro(a) Responsável: {dados['enfermeiro']}", ln=True)
    
    # Sinais Vitais (com borda)
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    sinais = f"PA: {dados['pa']} | Saturação: {dados['saturacao']}% | Escala de Dor: {dados['dor']}"
    pdf.cell(0, 10, txt=sinais, ln=True, border=1, align='C')
    
    # Evolução Clínica com multi_cell (Quebra de linha automática)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Evolução Clínica Detalhada:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(w=0, h=8, txt=dados['evolucao'], border=0, align='J')
    
    # Rodapé simples com data
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, txt="Documento gerado pelo Sistema de Gestão de Enfermagem.", align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- EXECUÇÃO DO APP ---
if verificar_login():
    # Só mostra o conteúdo abaixo se o login estiver correto
    st.sidebar.button("Sair", on_click=lambda: st.session_state.update({"autenticado": False}))
    
    st.title("🩺 Gestão de Enfermagem Especializada")
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
            dados_visita = {
                "paciente": nome_paciente, "enfermeiro": enfermeiro,
                "pa": pa, "saturacao": saturacao, "dor": dor, "evolucao": evolucao_texto
            }
            
            try:
                pdf_bytes = gerar_pdf(dados_visita)
                st.success("PDF pronto!")
                st.download_button(
                    label="📥 Baixar Relatório",
                    data=pdf_bytes,
                    file_name=f"relatorio_{nome_paciente}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
        else:
            st.warning("Preencha os campos obrigatórios (Nome e Evolução).")






