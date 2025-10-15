from app.extensions import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class MetodosPago(db.Model):
    __tablename__ = "metodospago"

    idmetodo = Column(Integer, primary_key=True, autoincrement=True)
    nombremetodo = Column(String, nullable=False)