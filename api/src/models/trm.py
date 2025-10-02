import uuid

from sqlalchemy import Column, Date, Float, String
from src.models.base import Base


class TRM(Base):
    __tablename__ = "trm"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
