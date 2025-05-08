import os

# Configuração do modelo Sabia
SABIA_API_URL = "https://api.sabia.ai/v1"

# Configurações do Qdrant
URL = "http://localhost:6333"
COLLECTION_NAME = "e5t30p"
#COLLECTION_NAME = "labset30p"
#COLLECTION_NAME = "bge3t30p2"
#COLLECTION_NAME = "bertimbaut30p"

HUGGINGFACE_MODEL = "intfloat/multilingual-e5-large"
#HUGGINGFACE_MODEL = "sentence-transformers/LaBSE"
#HUGGINGFACE_MODEL = "BAAI/bge-m3"
#HUGGINGFACE_MODEL = "neuralmind/bert-base-portuguese-cased"

#- intfloat/multilingual-e5-large - **BANCO:** e530p1
#- sentence-transformers/LaBSE - **BANCO:** labse30p
#- BAAI/bge-m3 - **BANCO:** bge3teste1
#- neuralmind/bert-base-portuguese-cased - **BANCO:** bertimbauteste1

# CONFIGURAÇÕES CHROMA:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")

# Parâmetros de chunking
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300

# Nome do modelo SABIA-3
SABIA_MODEL_NAME = "sabia-3"
SABIA_TOKEN = "104224658738889011687_558189197bfd43cb"
OPENAI_API_KEY = "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"