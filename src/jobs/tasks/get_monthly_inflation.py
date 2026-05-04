import asyncio
import logging
import os
from datetime import datetime

import requests

from src.db.session import database_session
from src.schemas.inflation import InflationData
from src.use_cases.inflation import InflationUseCase

logger = logging.getLogger(__name__)

INFLATION_WEB_SERVICE_URL: str | None = os.environ.get("INFLATION_WEB_SERVICE_URL")
if not INFLATION_WEB_SERVICE_URL:
    raise OSError("INFLATION_WEB_SERVICE_URL environment variable is required.")

_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,es-CO;q=0.8,es;q=0.7",
    "connection": "keep-alive",
    "content-type": "application/json; charset=utf-8",
    "referer": "https://suameca.banrep.gov.co/estadisticas-economicas/informacionSerie/100001/inflacion_y_meta",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "sec-ch-ua": '"Brave";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


def get_monthly_inflation() -> dict:
    try:
        response = requests.get(url=INFLATION_WEB_SERVICE_URL, headers=_HEADERS)
        response.raise_for_status()
        data = response.json()
        last_month_target = data.get("SERIES", {})[0].get("data").pop()
        last_month_inflation = data.get("SERIES", {})[1].get("data").pop()

        target = last_month_target[1]
        inflation = last_month_inflation[1]

        inflation_date_timestamp = last_month_inflation[0]
        dt_object = datetime.fromtimestamp(inflation_date_timestamp / 1000)

        inflation_data = {
            "year": dt_object.year,
            "month": dt_object.month,
            "target": target,
            "inflation": inflation,
        }

        logger.info(f"[get_monthly_inflation] Fetched data: {inflation_data}")
        return inflation_data
    except requests.RequestException as exc:
        logger.error(f"[get_monthly_inflation] Request failed: {exc}")
        raise
    except ValueError as exc:
        logger.error(f"[get_monthly_inflation] JSON decoding failed: {exc}")
        raise


def insert_monthly_inflation_into_db(inflation_data: dict) -> None:
    inflation_data_obj = InflationData(
        year=inflation_data["year"],
        month=inflation_data["month"],
        target=inflation_data["target"],
        annual_inflation_rate=inflation_data["inflation"],
    )

    async def _insert():
        db = next(database_session.get_db())
        try:
            use_case = InflationUseCase(db)
            await use_case.insert_inflation_data(inflation_data_obj)
        finally:
            db.close()

    asyncio.run(_insert())


def get_monthly_inflation_job():
    inflation_data = get_monthly_inflation()
    insert_monthly_inflation_into_db(inflation_data)
