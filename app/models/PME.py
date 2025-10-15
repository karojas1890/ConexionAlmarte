from app.extensions import db
from sqlalchemy import Column, Integer, String, Date,ForeignKey
from sqlalchemy.orm import relationship

class PME(db.Model):
    __tablename__ = "pme"

    identificacion = Column(String, primary_key=True)
    tutor = Column(String, ForeignKey("consultante.identificacion", ondelete="CASCADE", onupdate="CASCADE"))
    nombre = Column(String(100))
    apellido1 = Column(String(100))
    apellido2 = Column(String(100))
    telefono = Column(String(50))
    correo = Column(String(100))
    provincia = Column(String(100))
    canton = Column(String(100))
    distrito = Column(String(100))
    direccion_exacta = Column(String(200))
    fecha_nacimiento = Column(Date)
    edad = Column(Integer)
    escolaridad = Column(Integer)
    centro_educativo = Column(String(150))
    parentezco_tutor = Column(Integer)

    tutor_rel = relationship("Consultante", backref="pmes")