from app.extensions import db
from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, SmallInteger, func


class Sinpe(db.Model):
    __tablename__ = "sinpe"

    nreferencia = Column(BigInteger, primary_key=True, autoincrement=True)
    ntelefono = Column(String(15), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    fechahora = Column(DateTime, nullable=False, server_default=func.now())
    estado = Column(SmallInteger, nullable=False)

  