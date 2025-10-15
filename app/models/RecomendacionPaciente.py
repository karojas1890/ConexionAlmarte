
from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class RecomendacionPaciente(db.Model):
    __tablename__ = "recomendacionpaciente"

    idasignacion = Column(Integer, primary_key=True, autoincrement=True)
    idrecomendacion = Column(Integer, ForeignKey("recomendacionesterapeuticas.idrecomendacion", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    duraciondias = Column(Integer)
    momento = Column(String)
    consultante=Column(String,ForeignKey("consultante.identificacion", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    recomendacion_rel = relationship("RecomendacionesTerapeuticas", backref="pacientes")
    
    colsultante_rel=relationship("Consultante",backref="consultante")
    
    