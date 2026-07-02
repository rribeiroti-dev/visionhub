from sqlalchemy.orm import Session
from models.analysis import AnalysisModel
from config.settings import logger

class AnalysisRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, analysis: AnalysisModel) -> AnalysisModel:
        """Salva um registro de análise no banco de dados."""
        try:
            self.db.add(analysis)
            self.db.commit()
            self.db.refresh(analysis)
            return analysis
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no repositório: {str(e)}")
            raise e

    def get_all(self, search_query: str = None, start_date=None, end_date=None):
        """Busca análises aplicando filtros dinâmicos de busca e período temporal."""
        try:
            query = self.db.query(AnalysisModel)
            
            if search_query:
                query = query.filter(
                    (AnalysisModel.descricao.ilike(f"%{search_query}%")) |
                    (AnalysisModel.objetos.ilike(f"%{search_query}%"))
                )
            
            if start_date:
                query = query.filter(AnalysisModel.created_at >= start_date)
            if end_date:
                query = query.filter(AnalysisModel.created_at <= end_date)
                
            return query.order_by(AnalysisModel.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Erro ao buscar análises: {str(e)}")
            return []

    def delete(self, analysis_id: int) -> bool:
        """Exclui um registro do histórico."""
        try:
            analysis = self.db.query(AnalysisModel).filter(AnalysisModel.id == analysis_id).first()
            if analysis:
                self.db.delete(analysis)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar análise {analysis_id}: {str(e)}")
            return False