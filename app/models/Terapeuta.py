from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship



# -----------------------------
# TABLA TERAPEUTA
# -----------------------------
class Terapeuta(db.Model):
    __tablename__ = "terapeuta"

    identificacion = Column(String, primary_key=True)
    idusuario = Column(Integer, ForeignKey("usuario.idusuario"), nullable=False)
    nombre = Column(String, nullable=False)
    apellido1 = Column(String, nullable=False)
    apellido2 = Column(String)
    correo = Column(String, nullable=False)
    codigoprofesional = Column(String)
    telefono=Column(String)
   
    usuario = relationship("Usuario", backref="terapeuta")
