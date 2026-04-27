import logging
import signal
import sys
import time
from pathlib import Path

import schedule

from src.jobs.tasks.get_daily_trm import get_daily_trm_job

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

LOCK_FILE = Path("/tmp/banrepco_scheduler.lock")


def acquire_lock() -> bool:
    if LOCK_FILE.exists():
        return False
    LOCK_FILE.write_text(str(sys.executable))
    return True


def release_lock() -> None:
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def register_jobs() -> None:
    schedule.every().day.at("00:00").do(get_daily_trm_job)
    logger.info("Jobs registered — scheduled daily at 00:00")


def run_scheduler() -> None:
    if not acquire_lock():
        logger.error("Another scheduler instance is running. Exiting.")
        sys.exit(1)
    logger.info("Scheduler started — singleton lock acquired")

    def cleanup(*_):
        logger.info("Shutting down scheduler...")
        release_lock()
        sys.exit(0)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    register_jobs()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
