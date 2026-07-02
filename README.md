# VisionHub Pro - Streamlit Computer Vision & Neon.tech

Sistema completo e unificado de Visão Computacional para captura de imagens por webcam via navegador, análise clássica de atributos espectrais e de imagem (com OpenCV) e persistência em nuvem distribuída utilizando PostgreSQL da Neon.tech.

## 🚀 Tecnologias Empregadas
- **Linguagem Principal:** Python 3.12+
- **Interface Gráfica de Usuário:** Streamlit
- **Engine Core de Visão:** OpenCV (Open Source Computer Vision Library)
- **Persistência de Dados e ORM:** SQLAlchemy & Driver Psycopg3
- **Banco de Dados Cloud:** Neon.tech (PostgreSQL Serverless)
- **Plataforma PaaS de Deploy:** Render

## 🏗️ Arquitetura Arquitetural Aplicada
O projeto adota os preceitos de **Clean Architecture** e isolamento transacional de camadas:
1. **Models:** Mapeamento conceitual relacional das entidades de negócio.
2. **Repositories:** Abstração total de queries de banco de dados e operações CRUD.
3. **Services:** Centralização lógica das regras e execuções de algoritmos OpenCV.
4. **Interface (Views):** Framework Streamlit reagindo a interações em tempo real.

## 🛠️ Configuração Inicial e Execução Local

Como este projeto foi desenhado sob especificações corporativas estritas, **não é necessário criar ambientes virtuais (venv)**. O gerenciador de pacotes global do sistema pode ser utilizado.

### 1. Clonar o repositório
```bash
git clone <seu-repositorio-github>
cd computer-vision-streamlit