from datetime import date

from fastapi import Query
from fastapi_pagination import Params
from pydantic import BaseModel, Field


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


class TRMPaginateParams(Params):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(25, ge=1, le=100, description="Page size")
