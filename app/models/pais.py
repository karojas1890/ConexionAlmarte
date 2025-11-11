from app.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func  # para usar CURRENT_TIMESTAMP

class Pais(db.Model):
    __tablename__ = "pais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    codigo_iso = Column(String(3), nullable=False, unique=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())