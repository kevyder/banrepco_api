from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from src.db.session import database_session
from src.schemas.trm import (TRMByDate, TRMByDateRange, TRMData,
                             TRMPaginateParams)
from src.use_cases.trm import TRMUseCase

router = APIRouter(prefix="/trm", tags=["trm"])


@router.get("", response_model=Page[TRMData])
async def get_trm_data(
    sort: Literal["asc", "desc"] = Query(
        default="desc",
        description="Sort order by date"
    ),
    params: TRMPaginateParams = Depends(),
    db_session: Session = Depends(database_session.get_db)
) -> Page[TRMData]:
    """
    Retrieve TRM data with pagination and sorting.

    Args:
        sort: Sort order by date ('asc' or 'desc')
        params: Pagination parameters (handled automatically by fastapi-pagination)
        db_session: Database session (injected by FastAPI)

    Returns:
        Paginated list of TRM data records with metadata
    """
    use_case = TRMUseCase(db_session)
    query = await use_case.get_paginated_trm_data(
        sort_order=sort,
    )
    return paginate(query, params)


@router.get("/by-date-range", response_model=Page[TRMData])
async def get_trm_by_date_range(
    date_range: TRMByDateRange = Depends(),
    sort: Literal["asc", "desc"] = Query(
        default="asc",
        description="Sort order by date"
    ),
    params: TRMPaginateParams = Depends(),
    db_session: Session = Depends(database_session.get_db)
) -> Page[TRMData]:
    """
    Retrieve TRM data within a date range with pagination and sorting.

    Args:
        date_range: Start and end dates for the range
        sort: Sort order by date ('asc' or 'desc')
        params: Pagination parameters
        db_session: Database session

    Returns:
        Paginated list of TRM data records within the specified date range
    """
    use_case = TRMUseCase(db_session)
    query = await use_case.get_trm_by_date_range(
        start_date=date_range.start_date,
        end_date=date_range.end_date,
        sort_order=sort
    )
    return paginate(query, params)


@router.get("/by-date", response_model=TRMData)
async def get_trm_by_date(
    query_date: TRMByDate = Depends(),
    db_session: Session = Depends(database_session.get_db)
) -> TRMData:
    """
    Retrieve TRM data for a specific date.

    Args:
        specific_date: The date to query TRM data for (format: YYYY-MM-DD)
        db_session: Database session (injected by FastAPI)

    Returns:
        TRM data for the specified date

    Raises:
        HTTPException: If no TRM data is found for the specified date
    """
    use_case = TRMUseCase(db_session)
    result = await use_case.get_trm_by_date(query_date.specific_date)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No TRM data found for date: {query_date.specific_date}"
        )

    return result
