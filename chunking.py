from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def split_text_with_langchain(document, file_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP, 
        length_function=len, 
        add_start_index=True
    )

    documents = splitter.split_documents(document)

    for doc in documents:
       doc.page_content = "Conteudo do documento " + document[0].metadata["source"] + ": " + doc.page_content

    return documents