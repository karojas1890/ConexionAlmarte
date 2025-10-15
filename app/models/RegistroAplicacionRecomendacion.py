from app.extensions import db
from sqlalchemy import Column, String,Integer, ForeignKey,TIMESTAMP
from sqlalchemy.orm import relationship

class RegistroAplicacionRecomendacion(db.Model):
    __tablename__ = "registroAplicacionrecomendacion"

    idregistro = Column(Integer, primary_key=True, autoincrement=True)
    recomendacionaplicada = Column(Integer, ForeignKey("recomendacionpaciente.idasignacion", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    efectividad = Column(Integer)
    animoantes = Column(Integer)
    animodespues = Column(Integer)
    bienestarantes = Column(Integer)
    bienestardespues = Column(Integer)
    fechahoraregistro = Column(TIMESTAMP)
    comentario= Column(String(500))

    recomendacion_paciente_rel = relationship("RecomendacionPaciente", backref="registro_aplicacion")
