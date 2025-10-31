from app.extensions import db
from datetime import datetime
from sqlalchemy import Column, Integer, String,  DateTime,ForeignKey

class RestriccionPassword(db.Model):
    __tablename__ = "restriccion_password"

    idregistro = Column(Integer, primary_key=True, autoincrement=True)
    idusuario = Column(Integer, ForeignKey('usuario.idusuario'), nullable=False)
    password_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    
    usuario = db.relationship("Usuario", backref="historial_passwords")
