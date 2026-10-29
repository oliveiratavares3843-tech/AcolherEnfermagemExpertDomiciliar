# Sistema de Gestão de Enfermagem Expert Domiciliar

Este é um sistema de nível de produção especializado para o controle, triagem e gestão de atendimentos de enfermagem domiciliar. A aplicação foi desenvolvida focando em precisão, agilidade no acompanhamento de pacientes e integridade dos dados clínicos.

## 🚀 Acesse o Sistema Online
O sistema está implantado e pronto para uso em produção através do link abaixo:
🔗 [Acesse a aplicação em tempo real](https://streamlit.app)

---

## 🛠️ Arquitetura e Tecnologias Utilizadas

A aplicação foi estruturada seguindo boas práticas de desenvolvimento de software, separando de forma clara as camadas de apresentação, lógica de negócios e persistência de dados.

* **Python (Core do Sistema):** Linguagem principal utilizada para implementar as regras de negócio complexas, fluxos de triagem e manipulação segura de dados de saúde.
* **Streamlit (Front-end & Dashboard):** Interface do usuário reativa e otimizada para o fluxo de trabalho de profissionais de saúde, permitindo tomadas de decisão rápidas através de visualizações limpas.
* **Pandas (Engenharia de Dados):** Utilizado para a manipulação, modelagem, filtragem e organização eficiente das estruturas de dados estruturados dos pacientes.
* **SQLite (Persistência & Banco de Dados):** Banco de dados relacional robusto configurado para garantir o armazenamento seguro, transações confiáveis e integridade referencial das informações médicas confidenciais.

---

## 🏗️ Padrões de Engenharia e Desafios Resolvidos

### 1. Modelagem de Dados e Consistência Relacional
O back-end em Python foi integrado ao **SQLite** utilizando boas práticas de modelagem de dados (como chaves primárias, estrangeiras e restrições de integridade). Isso garante que o histórico clínico, prontuários e evoluções médicas fiquem permanentemente vinculados ao paciente correto, impedindo falhas de sobreposição de dados sensíveis.

### 2. Gerenciamento de Estado e Reatividade
Através do **Streamlit**, foi implementada uma arquitetura que lida com o gerenciamento de estado da sessão de forma eficiente. O sistema atualiza os dashboards de atendimento e relatórios de triagem em tempo real à medida que novos registros de enfermagem são inseridos, sem a necessidade de recargas totais pesadas na página.

### 3. Segurança e Validação de Inputs
A aplicação conta com camadas de validação de dados utilizando Python para garantir que campos críticos (como sinais vitais, dosagens e dados de identificação) sejam inseridos no formato correto antes de atingirem a camada do banco de dados, mitigando erros humanos na operação.

---

## 📦 Como Executar o Projeto Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com
   ```
2. Entre no diretório do projeto:
   ```bash
   cd AcolhimentoEnfermagemExpertDomiciliar
   ```
3. Instale as dependências listadas no `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

linkedink
