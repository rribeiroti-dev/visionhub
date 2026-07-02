import pandas as pd
import json

class FileExporter:
    @staticmethod
    def to_csv(analyses) -> bytes:
        """Gera arquivo estruturado em memória estruturado em CSV."""
        data = []
        for a in analyses:
            data.append({
                "ID": a.id,
                "Data": a.created_at,
                "Descricao": a.descricao,
                "Objetos": a.objetos,
                "Pessoas": a.quantidade_pessoas,
                "Rostos": a.rostos,
                "Luminosidade": a.luminosidade,
                "Nitidez": a.nitidez,
                "Cores": a.cores
            })
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode('utf-8')

    @staticmethod
    def to_json(analyses) -> str:
        """Gera dumping textual formatado em padrão estruturado JSON."""
        data = []
        for a in analyses:
            data.append({
                "id": a.id,
                "created_at": a.created_at.isoformat(),
                "image_path": a.image_path,
                "descricao": a.descricao,
                "objetos": a.objetos,
                "quantidade_pessoas": a.quantidade_pessoas,
                "rostos": a.rostos,
                "luminosidade": a.luminosidade,
                "nitidez": a.nitidez,
                "cores": a.cores,
                "extra": a.json_resultado
            })
        return json.dumps(data, indent=4, ensure_ascii=False)