from app.extensions import db
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

class Diario(db.Model):
    __tablename__ = "diario"

    Idregistro = Column(Integer, primary_key=True, autoincrement=True)
    fechahoraregistro = Column(TIMESTAMP)
    tiporegistro = Column(Integer)  # 0=Disparador,1=Avance
    descripcionevento = Column(String(1000))
    emocion = Column(Integer, ForeignKey("emociones.identificador", ondelete="CASCADE", onupdate="CASCADE"))
    conductaafrontamiento = Column(Integer, ForeignKey("conductasafrontamiento.identificador", ondelete="CASCADE", onupdate="CASCADE"))
    estrategiaaplicada = Column(Integer, ForeignKey("recomendacionpaciente.idasignacion", ondelete="CASCADE", onupdate="CASCADE"))
    efectividad = Column(Integer)

    emocion_rel = relationship("Emociones")
    conducta_rel = relationship("ConductasAfrontamiento")
    estrategia_rel = relationship("RecomendacionPaciente")