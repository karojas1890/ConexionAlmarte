from app.extensions import db
from sqlalchemy import Column, Integer, String,DateTime,Boolean,SmallInteger
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
class Auditoria(db.Model):
    __tablename__ = "auditoria"

    id_actividad = Column(Integer, primary_key=True, autoincrement=True)
    identificacion_consultante = Column(String(20), nullable=False)
    tipo_actividad = Column(SmallInteger, nullable=False)
    descripcion = Column(db.Text)
    codigo = Column(String(10))
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_origen = Column(String(45))
    dispositivo = Column(String(500))
    ubicacion = Column(String(100))
    datos_modificados = Column(JSONB)
    exito = Column(Boolean, default=True)
