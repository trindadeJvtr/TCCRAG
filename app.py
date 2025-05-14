import streamlit as st
from query_engine import chat_with_question

st.title("Chatbot Fusion Platform 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Faça uma consulta à documentação do Fusion!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_question(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
