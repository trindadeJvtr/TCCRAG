import streamlit as st
from query_engine import chat_with_question
from embeddings import insert_document

st.set_page_config(page_title="Chat com RAG", layout="wide")
st.html("<style> .main {overflow: hidden} </style>")

def processar_mensagem(mensagem):
    with st.container():
        with st.spinner("Pensando..."):
            return chat_with_question(mensagem)

# Inicializa histórico se não existir
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Função chamada ao enviar a pergunta
def enviar_mensagem():
    mensagem = st.session_state["mensagem"]
    if mensagem.strip() == "":
        return
    st.session_state.chat_history.append(("Você", mensagem, "user"))
    resposta = processar_mensagem(mensagem)
    st.session_state.chat_history.append(("RAG", resposta, "bot"))
    st.session_state["mensagem"] = ""  # Limpa o campo após envio

# Interface
with st.container():
    st.title("💬 Chatbot para consulta da documentação do Fusion Platform 🤖")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_input("Digite sua pergunta:", key="mensagem", label_visibility="collapsed")
    with col2:
        st.button("Enviar", on_click=enviar_mensagem, use_container_width=True)

with st.container(height=600):
    for remetente, msg, classe in reversed(st.session_state.chat_history):
        if classe == "bot":
            st.info(f"**{remetente}:** {msg}")
        else:
            st.warning(f"**{remetente}:** {msg}")
