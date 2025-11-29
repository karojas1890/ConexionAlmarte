from app.extensions import db
from sqlalchemy import Column, BigInteger, String, CHAR, SmallInteger, Numeric
from sqlalchemy.orm import validates
from datetime import datetime


class Tarjetas(db.Model):
    __tablename__ = "apitarjetas"

    numerotarjeta = Column(BigInteger, primary_key=True, nullable=False)
    nombretarjetahabiente = Column(String(150), nullable=False)
    identificaciontarjetahabiente = Column(String(20), nullable=False)
    codigoseguridad = Column(CHAR(3), nullable=False)

    mesexpira = Column(SmallInteger, nullable=False)
    annoexpira = Column(SmallInteger, nullable=False)

    saldo = Column(Numeric(12, 2), nullable=False, default=0)
    estado = Column(SmallInteger, nullable=False)