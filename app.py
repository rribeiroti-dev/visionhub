import streamlit as st
import os
from datetime import datetime, date
from PIL import Image
from database.connection import init_db, SessionLocal
from repositories.analysis_repository import AnalysisRepository
from services.cv_service import ComputerVisionService
from utils.file_exporter import FileExporter

# 1. Configuração da Página do Streamlit
st.set_page_config(
    page_title="VisionHub Pro - Web Cam Intel",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa banco de dados remotamente (Neon.tech)
init_db()

# Sessão do Banco vinculada ao ciclo de execução do script Streamlit
db_session = SessionLocal()
repo = AnalysisRepository(db_session)

# 2. Barra Lateral de Configurações e Estado
st.sidebar.title("📸 VisionHub Core")
st.sidebar.markdown("---")

# Validação visual do status de conexão
if db_session.bind:
    st.sidebar.success("● Conectado ao Neon.tech (PostgreSQL)")
else:
    st.sidebar.error("○ Desconectado do Banco de Dados")

st.sidebar.markdown("### Navegação Rápida")
app_mode = st.sidebar.radio("Selecione a tela ativa:", ["Captura em Tempo Real", "Histórico de Análises", "Indicadores Dashboard"])

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido por Arquiteto Full Stack Python v3.12")

# 3. Fluxo Principal do Aplicativo
if app_mode == "Captura em Tempo Real":
    st.title("📹 Captura de Imagem e Telemetria em Tempo Real")
    st.write("Acione a câmera integrada abaixo para efetuar análises computacionais instantâneas.")
    
    # Renderização da Câmera nativa via navegador usando componentes nativos do Streamlit
    img_file = st.camera_input("Alinhe o objeto/rosto na área delimitada:")
    
    if img_file is not None:
        bytes_data = img_file.getvalue()
        
        st.subheader("📸 Captura Registrada")
        st.image(bytes_data, caption="Foto para processamento", width=450)
        
        with st.spinner("Executando pipelines de análise matemática e espectral OpenCV..."):
            try:
                # Dispara a análise e salva em disco local + Neon.tech
                analysis_result = ComputerVisionService.analyze_image(bytes_data)
                saved_entity = repo.save(analysis_result)
                
                st.success("Análise persistida com sucesso no banco de dados distribuído Neon!")
                
                # Exibição dos resultados métricos
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="Rostos Mapeados", value=saved_entity.rostos)
                    st.metric(label="Luminosidade Média", value=f"{saved_entity.luminosidade} lx")
                with col2:
                    st.metric(label="Pessoas Estimadas", value=saved_entity.quantidade_pessoas)
                    st.metric(label="Fator de Nitidez", value=f"{saved_entity.nitidez} u")
                with col3:
                    st.metric(label="Cores Predominantes", value=saved_entity.cores)
                    st.metric(label="Resolução", value=saved_entity.json_resultado["metadata"]["resolucao"])
                
                st.info(f"**Descrição Gerada:** {saved_entity.descricao}")
                
            except Exception as e:
                st.error(f"Erro durante a execução do pipeline analítico: {e}")

elif app_mode == "Histórico de Análises":
    st.title("🗄️ Histórico Analítico e Exportação")
    
    # Barra de Filtros
    col_s, col_d1, col_d2 = st.columns([2, 1, 1])
    with col_s:
        search = st.text_input("🔍 Filtrar por conteúdo detectado ou descrição:")
    with col_d1:
        start_d = st.date_input("Data Inicial", value=date(2026, 1, 1))
    with col_d2:
        end_d = st.date_input("Data Final", value=date.today())
        
    # Converter datas para datetime para filtragem adequada no banco
    start_dt = datetime.combine(start_d, datetime.min.time())
    end_dt = datetime.combine(end_d, datetime.max.time())
    
    records = repo.get_all(search_query=search, start_date=start_dt, end_date=end_dt)
    
    if records:
        st.markdown("### Exportar Resultados Atuais")
        c_csv, c_json, _ = st.columns([1, 1, 4])
        
        with c_csv:
            csv_data = FileExporter.to_csv(records)
            st.download_button(label="📥 Baixar CSV", data=csv_data, file_name="analises.csv", mime="text/csv")
        with c_json:
            json_data = FileExporter.to_json(records)
            st.download_button(label="📥 Baixar JSON", data=json_data, file_name="analises.json", mime="application/json")
            
        st.markdown("---")
        
        # Renderização do grid do histórico
        for item in records:
            with st.container():
                c_img, c_txt, c_actions = st.columns([1, 2, 1])
                
                with c_img:
                    if os.path.exists(item.image_path):
                        img_display = Image.open(item.image_path)
                        st.image(img_display, use_container_width=True)
                    else:
                        st.warning("Arquivo físico local indisponível.")
                        
                with c_txt:
                    st.write(f"**ID: #{item.id}** — *Registrado em:* {item.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
                    st.write(f"**Descrição:** {item.descricao}")
                    st.write(f"**Objetos/Rostos:** {item.objetos} ({item.rostos} rostos)")
                    st.write(f"**Cores / Nitidez:** {item.cores} / {item.nitidez}")
                    
                with c_actions:
                    if os.path.exists(item.image_path):
                        with open(item.image_path, "rb") as file:
                            st.download_button(
                                label="Download Imagem",
                                data=file,
                                file_name=os.path.basename(item.image_path),
                                mime="image/jpeg",
                                key=f"dl_{item.id}"
                            )
                    if st.button("Excluir Registro", key=f"del_{item.id}"):
                        if repo.delete(item.id):
                            st.success(f"Registro {item.id} removido. Atualize a página.")
                            
                st.markdown("<hr style='margin:1em 0; border:0; border-top:1px solid #ddd;' />", unsafe_allow_html=True)
    else:
        st.info("Nenhum registro encontrado para os filtros aplicados.")

elif app_mode == "Indicadores Dashboard":
    st.title("📊 Painel de Controle e Métricas Gerais")
    all_data = repo.get_all()
    
    if all_data:
        total_capturas = len(all_data)
        total_rostos = sum([item.rostos for item in all_data])
        media_nitidez = sum([item.nitidez for item in all_data]) / total_capturas
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total de Capturas Processadas", total_capturas)
        col_m2.metric("Total de Rostos Catalogados", total_rostos)
        col_m3.metric("Média Espectral de Nitidez", f"{media_nitidez:.2f} u")
        
        # Lista estruturada rápida
        st.markdown("### Últimas Ocorrências")
        st.dataframe([
            {"ID": i.id, "Data": i.created_at, "Rostos": i.rostos, "Nitidez": i.nitidez, "Cores": i.cores}
            for i in all_data[:10]
        ], use_container_width=True)
    else:
        st.info("Banco vazio. Execute capturas para visualizar o painel analítico gráfico.")

# Fechar sessão de conexão ao finalizar renderização do bloco
db_session.close()