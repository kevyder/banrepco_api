import asyncio
import datetime
import logging
import os

import requests
import xmltodict

from src.db.session import database_session
from src.schemas.trm import TRMData
from src.use_cases.trm import TRMUseCase

logger = logging.getLogger(__name__)

BANREP_WEB_SERVICE_URL = os.environ.get("BANREP_WEB_SERVICE_URL")
if not BANREP_WEB_SERVICE_URL:
    raise EnvironmentError("BANREP_WEB_SERVICE_URL environment variable is required.")

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    "Accept": "*/*",
    "Referer": BANREP_WEB_SERVICE_URL,
}


def get_daily_trm() -> tuple[datetime.date, float]:
    url = f"{BANREP_WEB_SERVICE_URL}/ESTAT,DF_TRM_DAILY_LATEST,1.0/"

    for attempt in range(1, 4):
        try:
            response = requests.get(url, headers=_HEADERS, allow_redirects=True)
            response.raise_for_status()

            logger.info(f"[get_daily_trm] Attempt {attempt}/3 — status={response.status_code}, body_preview={response.text[:300]}")
            content_type = response.headers.get("Content-Type", "")
            if "xml" not in content_type.lower():
                raise ValueError(f"Unexpected Content-Type: {content_type}")

            parsed = xmltodict.parse(response.text, process_namespaces=False)
            obs = (
                parsed["message:GenericData"]
                ["message:DataSet"]
                ["generic:Series"]
                ["generic:Obs"]
            )
            raw_date = obs["generic:ObsDimension"]["@value"]
            raw_value = obs["generic:ObsValue"]["@value"]

            if raw_value is None:
                raise ValueError("TRM value is null")

            trm_date = datetime.datetime.strptime(raw_date, "%Y%m%d").date()
            trm_value = float(raw_value)
            logger.info(f"[get_daily_trm] Fetched TRM: date={trm_date}, value={trm_value}")
            return trm_date, trm_value

        except (requests.RequestException, ValueError, KeyError) as exc:
            logger.warning(f"[get_daily_trm] Attempt {attempt}/3 failed: {exc}")
            if attempt == 3:
                logger.error("[get_daily_trm] All 3 attempts exhausted")
                raise

    raise RuntimeError("unreachable")


def insert_trm_into_db(trm_date: datetime.date, trm_value: float) -> None:
    trm_data = TRMData(date=trm_date, value=trm_value)

    async def _insert():
        db = next(database_session.get_db())
        try:
            use_case = TRMUseCase(db)
            await use_case.insert_trm_data(trm_data)
        finally:
            db.close()

    asyncio.run(_insert())


def get_daily_trm_job() -> None:
    trm_date, trm_value = get_daily_trm()
    insert_trm_into_db(trm_date, trm_value)
