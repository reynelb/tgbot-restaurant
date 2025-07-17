from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    date = Column(String)
    time = Column(String)
    people = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class PreOrder(Base):
    __tablename__ = "preorders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    dishes = Column(String)  # Guardamos como texto separado por comas
    created_at = Column(DateTime, default=datetime.utcnow)
