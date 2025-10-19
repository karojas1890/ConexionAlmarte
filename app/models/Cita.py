from app.extensions import db
from sqlalchemy import Column, Integer, String,ForeignKey,Float,TIMESTAMP
from sqlalchemy.orm import relationship

class Citas(db.Model):
    __tablename__ = "citas"

    citaid = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String, ForeignKey("consultante.identificacion", ondelete="CASCADE", onupdate="CASCADE"))
    servicio = Column(Integer, ForeignKey("servicios.idservicio", ondelete="CASCADE", onupdate="CASCADE"))
    iddisponibilidad = Column(Integer, ForeignKey("disponibilidad.iddisponibilidad", ondelete="CASCADE", onupdate="CASCADE"))
    estado = Column(Integer, default=0)  
    pago = Column(Integer, default=1)   

    consultante_Cita = relationship("Consultante")
    servicio_Cita= relationship("servicios")
    disponibilidad_Cita = relationship("Disponibilidad")
