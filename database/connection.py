from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import get_database_url, logger

# Volta a ler a URL oficial que configuraremos no painel do Render
DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL, 
    pool_size=5, 
    max_overflow=10, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    try:
        logger.info("Tentando sincronizar e criar tabelas no Neon.tech...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas verificadas/criadas com sucesso.")
    except Exception as e:
        logger.critical(f"Falha ao inicializar o banco de dados: {str(e)}")