from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class RecursosApoyo(db.Model):
    __tablename__ = "recursosapoyo"

    idrecurso = Column(Integer, primary_key=True, autoincrement=True)
    nombrerecurso = Column(String, nullable=False)
    urlrecurso = Column(String)
    duracionminutos = Column(Integer)
    recomendacion = Column(Integer, ForeignKey("recomendacionesterapeuticas.idrecomendacion", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    recomendacion_Apoyo = relationship("RecomendacionesTerapeuticas", backref="recursos")
