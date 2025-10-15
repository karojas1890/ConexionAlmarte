from app.extensions import db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Time, ForeignKey
from sqlalchemy.orm import relationship


class Usuario(db.Model):
    __tablename__ = "usuario"

    idusuario = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    codigo6digitos = Column(String)
    estado = Column(Integer, default=1)  # 1 activo, 0 inactivo
    tipo = Column(Integer)  # 1=Consultante, 2=Terapeuta
    intentos = Column(Integer)
