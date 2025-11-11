from app.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class EstadoProvincia(db.Model):
    __tablename__ = "estado_provincia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pais_id = Column(Integer, ForeignKey("pais.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

   
    pais = relationship("Pais", backref="estados_provincias")
