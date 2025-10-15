from app.extensions import db
from sqlalchemy import Column, Integer, String,  Date, Time, ForeignKey
from sqlalchemy.orm import relationship

class Disponibilidad(db.Model):
    __tablename__ = "disponibilidad"

    iddisponibilidad = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    horainicio = Column(Time, nullable=False)
    horafin = Column(Time, nullable=False)
    estado = Column(Integer, default=1)  # 1=Disponible,2=Reservado,3=Bloqueado
    idterapeuta = Column(String, ForeignKey("terapeuta.identificacion", ondelete="CASCADE", onupdate="CASCADE"))

    terapeuta_rel = relationship("Terapeuta", backref="disponibilidades")