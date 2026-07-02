import cv2
import numpy as np
from datetime import datetime
from PIL import Image
from models.analysis import AnalysisModel
from config.settings import UPLOAD_FOLDER, logger

class ComputerVisionService:
    @staticmethod
    def analyze_image(image_bytes: bytes) -> AnalysisModel:
        """
        Executa o processamento heurístico e de visão computacional clássica (OpenCV)
        sobre a imagem extraída da webcam. Pronto para injeção de LLMs/VLM.
        """
        now = datetime.now()
        filename = f"capture_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
        file_path = UPLOAD_FOLDER / filename

        # Salvar o arquivo no disco rígido local
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # Converter bytes para formato OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Falha ao decodificar matriz de imagem.")

        height, width, _ = img.shape
        resolution_str = f"{width}x{height}"

        # 1. Medição de Luminosidade
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        luminosity = float(np.mean(gray))

        # 2. Medição de Nitidez (Variância do Laplaciano)
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        # 3. Análise Algorítmica de Rostos (Haar Cascade Embutido)
        # Utiliza o modelo clássico do OpenCV distribuído nativamente
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)
        faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        num_faces = len(faces_detected)

        # Heurística preliminar de contagem populacional baseada em faces detectadas
        num_people = num_faces 

        # 4. Extração de Paleta de Cores Predominante
        # Resize para otimização de processamento rápido do K-Means simplificado
        small_img = cv2.resize(img, (50, 50), interpolation=cv2.INTER_AREA)
        pixels = small_img.reshape(-1, 3)
        counts = np.bincount(np.argmax(pixels, axis=1), minlength=3)
        
        # Mapeamento elementar de canais BGR para texto
        color_map = {0: "Tonalidades Azuis", 1: "Tonalidades Verdes", 2: "Tonalidades Vermelhas"}
        dominant_color = color_map.get(int(np.argmax(counts)), "Mistas/Neutras")

        # Mock Estruturado de Extensibilidade para Inteligências Artificiais Generativas
        # (OpenAI, Gemini, Ollama podem substituir as tags estruturadas abaixo facilmente)
        detected_objects = ["Pessoa"] if num_faces > 0 else ["Ambiente de captura / Objeto Geral"]
        description = f"Captura em ambiente com iluminação de {luminosity:.1f} lx e foco calculado em {sharpness:.1f} unidades."

        # Construção da Entidade de Persistência
        analysis = AnalysisModel(
            created_at=now,
            image_path=str(file_path),
            descricao=description,
            objetos=", ".join(detected_objects),
            quantidade_pessoas=num_people,
            rostos=num_faces,
            idade="Suporte I.A. Pendente",
            emocao="Suporte I.A. Pendente",
            cores=dominant_color,
            luminosidade=round(luminosity, 2),
            nitidez=round(sharpness, 2),
            json_resultado={
                "metadata": {
                    "software_engine": "OpenCV Clássico",
                    "resolucao": resolution_str,
                    "canais_cor": "BGR",
                    "timestamp_unix": now.timestamp()
                }
            }
        )
        
        logger.info(f"Análise efetuada com sucesso para o arquivo {filename}.")
        return analysis