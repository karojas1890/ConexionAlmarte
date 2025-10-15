from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class RecomendacionesTerapeuticas(db.Model):
    __tablename__ = "recomendacionesterapeuticas"

    idrecomendacion = Column(Integer, primary_key=True, autoincrement=True)
    idcategoria = Column(Integer, ForeignKey("categoriasrecomendaciones.intcategoria", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    nombrerecomendacion = Column(String, nullable=False)
    descripcion = Column(String)
    urlimagen = Column(String)
    duracionminutos=Column(Integer)
    
    categoria_r = relationship("CategoriasRecomendaciones", backref="recomendaciones")
    