from uuid import UUID

from pydantic import BaseModel, Field


class InflationData(BaseModel):
    id: UUID
    year: int
    month: int
    inflation_rate: float
    target: float | None

    class Config:
        from_attributes = True


class InflationDateRange(BaseModel):
    start_year: int = Field(..., description="Start year for the date range", ge=1955, le=2100)
    start_month: int = Field(..., description="Start month for the date range", ge=1, le=12)
    end_year: int = Field(..., description="End year for the date range", ge=1955, le=2100)
    end_month: int = Field(..., description="End month for the date range", ge=1, le=12)
