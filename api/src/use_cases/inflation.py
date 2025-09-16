from typing import Literal

from sqlalchemy import asc, desc
from sqlalchemy.orm import Query, Session

from src.models.inflation import Inflation
from src.schemas.inflation import InflationData, InflationDateRange


class InflationUseCase:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_paginated_inflation_data(
        self,
        sort_order: Literal["asc", "desc"] = "desc",
    ) -> Query:
        """
        Get inflation data query with sorting and optional date range filtering.

        Args:
            sort_order: Sort order for year and month ('asc' or 'desc')
            from_date: Optional start date as (year, month)
            to_date: Optional end date as (year, month)

        Returns:
            SQLAlchemy Query object ready for pagination
        """
        query = self.db_session.query(Inflation)

        # Apply sorting
        if sort_order == "desc":
            query = query.order_by(desc(Inflation.year), desc(Inflation.month))
        else:
            query = query.order_by(asc(Inflation.year), asc(Inflation.month))

        return query

    def get_inflation_data_by_exact_date(
        self,
        year: int,
        month: int
    ) -> InflationData | None:
        """
        Get a specific inflation record by year and month.

        Args:
            year: The year to search for
            month: The month to search for (1-12)

        Returns:
            The inflation record if found, None otherwise
        """

        record = self.db_session.query(Inflation).filter(
            Inflation.year == year,
            Inflation.month == month
        ).first()

        inflation = InflationData.model_validate(record) if record else None

        return inflation

    def get_inflation_data_by_date_range(
        self,
        date_range: InflationDateRange,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> Query:
        """
        Get inflation data filtered by date range without pagination.

        Args:
            date_range: Date range parameters for filtering
            sort_order: Sort order for year and month ('asc' or 'desc')

        Returns:
            List of inflation data records within the specified date range
        """
        query = self.db_session.query(Inflation)

        # Apply date range filter
        query = query.filter(
            ((Inflation.year == date_range.start_year) & (Inflation.month >= date_range.start_month)) |
            (Inflation.year > date_range.start_year)
        ).filter(
            ((Inflation.year == date_range.end_year) & (Inflation.month <= date_range.end_month)) |
            (Inflation.year < date_range.end_year)
        )

        # Apply sorting
        if sort_order == "desc":
            query = query.order_by(desc(Inflation.year), desc(Inflation.month))
        else:
            query = query.order_by(asc(Inflation.year), asc(Inflation.month))

        return query
