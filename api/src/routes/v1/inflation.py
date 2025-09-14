from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src.db.session import db
from src.models.inflation import Inflation
from src.schemas.inflation import InflationData, InflationDateRange
from src.use_cases.inflation import InflationUseCase

router = APIRouter(prefix="/inflation", tags=["inflation"])


@router.get("/", response_model=Page[InflationData])
async def get_inflation_data(
    sort: Literal["asc", "desc"] = Query(
        default="desc",
        description="Sort order by year and month"
    ),
    params: Params = Depends(),
    db_session: Session = Depends(db.get_db)
) -> Page[InflationData]:
    """
    Retrieve inflation data with pagination, sorting, and date range filtering.

    Args:
        sort: Sort order by year and month ('asc' or 'desc')
        date_range: Date range parameters for filtering
        params: Pagination parameters (handled automatically by fastapi-pagination)
        db_session: Database session (injected by FastAPI)

    Returns:
        Paginated list of inflation data records with metadata
    """

    use_case = InflationUseCase(db_session)
    query = use_case.get_paginated_inflation_data(
        sort_order=sort,
    )
    return paginate(query, params)


@router.get("/{year}/{month}", response_model=InflationData)
async def get_inflation_data_by_date(
    year: int,
    month: int,
    db_session: Session = Depends(db.get_db)
) -> InflationData:
    """
    Retrieve a specific inflation record by year and month.

    Args:
        year: The year to get inflation data for (1955-2100)
        month: The month to get inflation data for (1-12)
        db_session: Database session (injected by FastAPI)

    Returns:
        The inflation record for the specified year and month

    Raises:
        HTTPException: If no record is found for the specified date
    """
    use_case = InflationUseCase(db_session)
    result = use_case.get_inflation_data_by_exact_date(year=year, month=month)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No inflation data found for {year}/{month}"
        )

    return result


@router.get("/date-range", response_model=list[InflationData])
async def get_inflation_data_by_date_range(
    date_range: InflationDateRange = Depends(),
    sort: Literal["asc", "desc"] = Query(
        default="asc",
        description="Sort order by year and month"
    ),
    db_session: Session = Depends(db.get_db)
) -> List[Inflation]:
    """
    Retrieve inflation data filtered by date range without pagination.

    Args:
        date_range: Date range parameters for filtering (year and month)
        sort: Sort order by year and month ('asc' or 'desc')
        db_session: Database session (injected by FastAPI)

    Returns:
        List of inflation data records within the specified date range
    """
    use_case = InflationUseCase(db_session)
    return use_case.get_inflation_data_by_date_range(
        date_range=date_range,
        sort_order=sort
    )
