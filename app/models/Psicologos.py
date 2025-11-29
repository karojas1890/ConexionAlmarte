from app.extensions import db
from sqlalchemy import Column, Integer, String, SmallInteger


class ProfesionalPsicologia(db.Model):
    __tablename__ = "profesionalpsicologia"

    codigoprofesional = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido1 = Column(String(100), nullable=False)
    apellido2 = Column(String(100), nullable=True)
    
    estadoresponsabilidadeconomica = Column(SmallInteger, nullable=False)
    estado = Column(SmallInteger, nullable=False)
    
    habilitacionesevaluaciones = Column(String(255), nullable=True)
    areatrabajo = Column(String(150), nullable=True)
