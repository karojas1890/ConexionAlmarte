from app.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class CiudadMunicipio(db.Model):
    __tablename__ = "ciudad_municipio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estado_provincia_id = Column(Integer, ForeignKey("estado_provincia.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    
    estado_provincia = relationship("EstadoProvincia", backref="ciudades_municipios")

   