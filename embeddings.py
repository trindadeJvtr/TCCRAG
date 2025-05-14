import json
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType

from chunking import split_text_with_langchain
from config import HUGGINGFACE_MODEL, PERSIST_DIR

def insert_document(directory_path):
    documents = []

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path) and check_type_files(filename):
                try:
                    loader = DoclingLoader(
                        file_path=file_path,
                        export_type=ExportType.MARKDOWN
                    )
                    document = loader.load()
                    document[0].metadata["source"] = filename
                    documents.append(document)
                except Exception as e:
                    print(f"Erro ao carregar o arquivo {filename}: {e}")

    print("Texto carregado:")
    all_chunks = []
    for document in documents:
        chunks = split_text_with_langchain(document, os.path.basename(file_path))
        all_chunks.extend(chunks)

    embeddings = HuggingFaceEmbeddings(model_name=HUGGINGFACE_MODEL)

    chroma_db = Chroma.from_documents(
        all_chunks,
        embedding=embeddings,
        persist_directory= "./chroma_db",
    )

    chroma_db.persist()

    query = "Como posso configurar quem terá acesso ao relatório que estou criando?"
    response = chroma_db.similarity_search(query, k=3)

    response_dicts = [doc.__dict__ for doc in response]
    json_output = json.dumps(response_dicts, indent=4, ensure_ascii=False)

    print(json_output)


def check_type_files(filename):
    return filename.endswith(".md") or filename.endswith(".pdf")
