import uuid

from sqlalchemy import Column, Float, Integer, String

from src.models.base import Base


class Inflation(Base):
    __tablename__ = "inflation"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    inflation_rate = Column(Float, nullable=False)
    target = Column(Float, nullable=True)
