from app.extensions import db
from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.orm import relationship


class Servicios(db.Model):
    __tablename__ = "servicios"

    idservicio = Column(Integer, primary_key=True, autoincrement=True)
    nombreservicio = Column(String(50), nullable=False)
    descripcionservicio = Column(String(100))
    urlimagen = Column(String)
    duracionHoras = Column(Integer)
    precio = Column(Float)