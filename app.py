import streamlit as st
from query_engine import chat_with_question
from embeddings import insert_document

st.set_page_config(page_title="Chat com RAG", layout="wide")

st.html("<style> .main {overflow: hidden} </style>")

def processar_mensagem(mensagem):
    with st.container():
        with st.spinner("Pensando..."):
            return chat_with_question(mensagem)

with st.container():
    st.title("💬 Chatbot para consulta da documentação do Fusion Platform 🤖")
    col1, col2 = st.columns([4, 1])
    with col1:
        mensagem = st.text_input("Digite sua pergunta:", key="mensagem", label_visibility="collapsed")
    with col2:
        enviar = st.button("Enviar", use_container_width=True)

    if enviar and mensagem:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append(("Você", mensagem, "user"))
        resposta = processar_mensagem(mensagem)
        st.session_state.chat_history.append(("RAG", resposta, "bot"))

    with st.container(height=600):
        if "chat_history" in st.session_state:
            for remetente, msg, classe in reversed(st.session_state.chat_history):
                if classe == "bot":
                    st.info(f"**{remetente}:** {msg}")
                else:
                    st.warning(f"**{remetente}:** {msg}")