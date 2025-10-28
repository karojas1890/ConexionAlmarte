from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class Tarjeta(db.Model):
    __tablename__ = "tarjetas"

    id_tarjeta = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.idusuario"), nullable=False)
    nombre_titular = Column(String(100), nullable=False)
    numero_tarjeta = Column(String(19), nullable=False)
    ultimo4 = Column(String(4), nullable=False)
    fecha_expiracion = Column(String(5), nullable=False)
    estado = Column(String(10), default='ACTIVO')
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", backref="tarjetas")
