import streamlit as st
from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from config import HUGGINGFACE_MODEL, OPENAI_API_KEY, PROJECT_ID


@st.cache_resource(show_spinner=False)
def carregar_embedding():
    return HuggingFaceEmbeddings(model_name=HUGGINGFACE_MODEL)


@st.cache_resource(show_spinner=False)
def carregar_chroma():
    embedding = carregar_embedding()
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding
    )


@st.cache_resource(show_spinner=False)
def carregar_openai():
    return OpenAI(api_key=OPENAI_API_KEY, project=PROJECT_ID)


def chat_with_question(question):
    query = question
    chroma_db = carregar_chroma()
    client = carregar_openai()

    docs = chroma_db.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt_template = PromptTemplate(
        input_variables=["context", "query"],
        template=(
            "Você é um atendente experiente no uso do sistema Fusion Platform. "
            "Explique a resposta para a pergunta a seguir com o máximo de detalhes possíveis, "
            "incluindo **configurações necessárias**, **passo a passo prático**, e **considerações importantes**. "
            "Organize a resposta em etapas claras, numeradas ou com marcadores. "
            "Evite jargões técnicos complexos sem explicação. "
            "Baseie-se apenas no conteúdo abaixo, e se a resposta não estiver clara no contexto, diga isso com sinceridade.\n\n"
            "### CONTEXTO:\n{context}\n\n"
            "### PERGUNTA:\n{query}\n\n"
            "### RESPOSTA DETALHADA:"
        )
    )

    prompt = prompt_template.format(context=context, query=query)

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Você é um atendente especializado no sistema Fusion Platform."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Erro durante execução: {e}")
        return "Erro ao processar a resposta."
