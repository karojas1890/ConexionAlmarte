from app.extensions import db
from sqlalchemy import Column, Integer, String, Date,ForeignKey
from sqlalchemy.orm import relationship


class Consultante(db.Model):
    __tablename__ = "consultante"

    identificacion = Column(String, primary_key=True)
    idusuario = Column(Integer, ForeignKey("usuario.idusuario"), nullable=False)
    nombre = Column(String, nullable=False)
    apellido1 = Column(String, nullable=False)
    apellido2 = Column(String)
    telefono = Column(String)
    correo = Column(String)
    provincia = Column(String)
    canton = Column(String)
    distrito = Column(String)
    direccionexacta = Column(String)
    fechanacimiento = Column(Date)
    edad = Column(Integer)
    ocupacion = Column(String)
    lugartrabajoestudio = Column(String)
    tipo = Column(Integer)  # 1=Paciente, 2=Tutor PME
    urlimagen = Column(String)
    
    usuario = relationship("Usuario", backref="consultante")
    