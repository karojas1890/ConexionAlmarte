from app.extensions import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Emociones(db.Model):
    __tablename__ = "emociones"

    identificador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
