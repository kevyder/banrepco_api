from datetime import date

from fastapi import Query
from fastapi_pagination import Params
from pydantic import BaseModel, Field, field_validator


class TRMData(BaseModel):
    date: date
    value: float

    class Config:
        from_attributes = True


class TRMByDate(BaseModel):
    specific_date: date = Query(description="Date to query for TRM data")


class TRMByDateRange(BaseModel):
    start_date: date = Field(..., description="Start date for the range")
    end_date: date = Field(..., description="End date for the range")

    @field_validator('end_date')
    @classmethod
    def validate_end_date_after_start(cls, v: date, values) -> date:
        if v < values.data['start_date']:
            raise ValueError("End date cannot be before start date.")
        return v


class TRMPaginateParams(Params):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(25, ge=1, le=100, description="Page size")
