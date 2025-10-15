from app.extensions import db
from sqlalchemy import Column, Integer, String


class ConductasAfrontamiento(db.Model):
    __tablename__ = "conductasafrontamiento"

    identificador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)