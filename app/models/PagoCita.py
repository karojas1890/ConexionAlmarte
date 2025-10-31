from app.extensions import db
from sqlalchemy import Column, Integer, Float, ForeignKey,TIMESTAMP
from sqlalchemy.orm import relationship

class PagosCita(db.Model):
    __tablename__ = "pagoscita"

    idpago = Column(Integer, primary_key=True, autoincrement=True)
    idcita = Column(Integer, ForeignKey("citas.citaid", ondelete="CASCADE", onupdate="CASCADE"))
    idmetodo = Column(Integer, ForeignKey("metodospago.idmetodo", ondelete="CASCADE", onupdate="CASCADE"))
    monto = Column(Float, nullable=False)
    fechapago = Column(TIMESTAMP)

    cita_rel = relationship("Citas", backref="pagos_rel")
    metodo_rel = relationship("MetodosPago", backref="pagos_rel")