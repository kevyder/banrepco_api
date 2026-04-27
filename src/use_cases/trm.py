from datetime import date
from typing import Literal

from sqlalchemy.orm import Session

from src.models.trm import TRM
from src.schemas.trm import TRMData


class TRMUseCase:
    """Use case for TRM (Tasa Representativa del Mercado) operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_paginated_trm_data(
        self,
        sort_order: Literal["asc", "desc"] = "desc",
    ):
        """
        Get paginated TRM data with optional sorting.

        Args:
            sort_order: Sort order by date ('asc' or 'desc')

        Returns:
            Query object for paginated TRM data
        """
        query = self.db_session.query(TRM)
        query = query.with_entities(TRM.date, TRM.value)

        if sort_order == "asc":
            query = query.order_by(TRM.date.asc())
        else:
            query = query.order_by(TRM.date.desc())

        return query

    async def get_trm_by_date(self, specific_date: date) -> TRMData | None:
        """
        Get TRM data for a specific date.

        Args:
            specific_date: The date to query for

        Returns:
            TRM data for the specified date if found, None otherwise
        """

        query = self.db_session.query(TRM)
        query = query.with_entities(TRM.date, TRM.value)
        record = query.filter(TRM.date == specific_date).first()

        trm = TRMData.model_validate(record) if record else None

        return trm

    async def get_trm_by_date_range(
        self,
        start_date: date,
        end_date: date,
        sort_order: Literal["asc", "desc"] = "desc"
    ):
        """
        Get TRM data for a specific date range.

        Args:
            start_date: Start date of the range
            end_date: End date of the range
            sort_order: Sort order by date ('asc' or 'desc')

        Returns:
            Query object for TRM data within the date range
        """

        query = self.db_session.query(TRM)
        query = query.with_entities(TRM.date, TRM.value)

        query = query.filter(
            TRM.date >= start_date,
            TRM.date <= end_date
        )

        if sort_order == "asc":
            query = query.order_by(TRM.date.asc())
        else:
            query = query.order_by(TRM.date.desc())

        return query

    async def insert_trm_data(self, trm_data: TRMData) -> None:
        """
        Insert a new TRM record into the database.

        Args:
            trm_data: The TRM data to insert
        """

        trm_existing_record = self.db_session.query(TRM).filter(TRM.date == trm_data.date).first()
        if trm_existing_record:
            return

        new_trm_record = TRM(date=trm_data.date, value=trm_data.value)
        self.db_session.add(new_trm_record)
        self.db_session.commit()
