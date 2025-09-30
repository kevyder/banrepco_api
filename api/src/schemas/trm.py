from datetime import date
from uuid import UUID

from pydantic import BaseModel


class InflationData(BaseModel):
    id: UUID
    date: date
    value: float

    class Config:
        from_attributes = True
