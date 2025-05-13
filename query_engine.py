import asyncio
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from config import SABIA_TOKEN, HUGGINGFACE_MODEL, PERSIST_DIR

def chat_with_question(question):
    query = question
    embedding = HuggingFaceEmbeddings(model_name=HUGGINGFACE_MODEL)

    llm = ChatOpenAI(
        model="sabia-3",
        temperature=0,
        api_key=SABIA_TOKEN,
        base_url="https://chat.maritaca.ai/api"
    )

    chroma_db = Chroma(
        persist_directory= PERSIST_DIR,
        embedding_function=embedding
    )

    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template=(
            "Se comporte como um atendente que tira duvidas sobre o sistema Fusion Platform. "
            "Responda a pergunta abaixo se baseando nessa parte retirada da documentação do fusion platform. "
            "Se você não encontrar a resposta no contexto disponibilizado, "
            "diga que não foi possível responder.\n\n"
            "{context}\n\n"
            "Pergunta: {query}"
        )
    )

    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt, verbose=True)
    docs = chroma_db.similarity_search(query, k=5)

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        answer = loop.run_until_complete(chain.ainvoke({"input_documents": docs, "query": query}))

        print("RESPOSTA DO CHAT:", answer["output_text"])
        return answer["output_text"]
    except Exception as e:
        print(f"Erro durante execução: {e}")
        return "Erro ao processar a resposta."
