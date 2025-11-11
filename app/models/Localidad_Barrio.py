from app.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class LocalidadBarrio(db.Model):
    __tablename__ = "localidad_barrio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ciudad_municipio_id = Column(Integer, ForeignKey("ciudad_municipio.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    codigo_postal = Column(String(20))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

   
    ciudad_municipio = relationship("CiudadMunicipio", backref="localidades_barrios")
