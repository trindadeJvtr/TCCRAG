import os
import streamlit as st

# Configuração do modelo Sabia
SABIA_API_URL = "https://api.sabia.ai/v1"

# Configurações do Qdrant
URL = "http://localhost:6333"
COLLECTION_NAME = "e5t30p"

HUGGINGFACE_MODEL = "intfloat/multilingual-e5-large"

# CONFIGURAÇÕES CHROMA:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")

# Parâmetros de chunking
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 400

# Nome do modelo SABIA-3
SABIA_MODEL_NAME = "sabia-3"

SABIA_TOKEN = st.secrets["SABIA_API_KEY"]