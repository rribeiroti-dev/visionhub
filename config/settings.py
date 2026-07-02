import os
import sys
import logging
from pathlib import Path
import streamlit as st

# Diretórios Base
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploaded_images"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

LOG_FILE = BASE_DIR / "app.log"

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)
logger = logging.getLogger("CVApp")

def get_database_url() -> str:
    """
    Recupera a URL do banco de dados priorizando variáveis de ambiente (Render)
    e depois st.secrets (Streamlit Cloud).
    """
    # 1. Tenta pegar primeiro da variável de ambiente padrão (Render)
    url = os.environ.get("DATABASE_URL", "")
    
    # 2. Se estiver vazia, tenta buscar com segurança no st.secrets (Local/Streamlit Cloud)
    if not url:
        try:
            if "DATABASE_URL" in st.secrets:
                url = st.secrets["DATABASE_URL"]
        except Exception:
            # Caso não haja secrets configurados, evita que a aplicação quebre
            pass

    # Ajuste automático de compatibilidade do driver do SQLAlchemy
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        
    return url
