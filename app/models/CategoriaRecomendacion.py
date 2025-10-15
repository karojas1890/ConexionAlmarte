from app.extensions import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class CategoriasRecomendaciones(db.Model):
    __tablename__ = "categoriasrecomendaciones"

    intcategoria = Column(Integer, primary_key=True, autoincrement=True)
    nombrecategoria = Column(String, nullable=False)
    descripcioncategoria = Column(String)
    
    
