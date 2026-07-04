# app/workers/queue.py
import os
from datetime import datetime, timezone
from uuid import UUID

from arq.connections import RedisSettings

from app.config.settings import settings
from app.database.connection import AsyncSessionLocal
from app.services.recommendation import recommendation_service
from app.utils.logger import logger


def _save_report_to_disk(work_req_id: UUID, report_json: str) -> str:
    """Persist the report JSON under REPORTS_DIR/{work_req_id}/{timestamp}.json."""
    dir_path = os.path.join(settings.REPORTS_DIR, str(work_req_id))
    os.makedirs(dir_path, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    file_path = os.path.join(dir_path, f"{timestamp}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_json)
    return file_path


async def generate_report_task(ctx, work_req_id: UUID):
    """Background task to generate an AI report for a work requirement."""
    logger.info(f"Starting background report generation for Work Req: {work_req_id}")

    # We must create a fresh DB session for the background worker
    async with AsyncSessionLocal() as db:
        report = await recommendation_service.generate_report(db, work_req_id)
        if report is None:
            return None

        report_json = report.model_dump_json(indent=2)

        # MVP persistence: write to local reports/ folder.
        # Production: swap for a DB table (ai_reports) or object storage.
        try:
            saved_path = _save_report_to_disk(work_req_id, report_json)
            logger.info(f"Report saved to {saved_path}")
        except OSError as e:
            logger.error(f"Failed to write report file: {e}")
            saved_path = None

        logger.info("\n" + "=" * 50 + "\nAI VENDOR JUSTIFICATION REPORT\n" + "=" * 50)
        logger.info(report_json)
        logger.info("=" * 50)

        return {
            "report": report.model_dump(mode="json"),
            "saved_path": saved_path,
        }


# ARQ worker settings
class WorkerSettings:
    functions = [generate_report_task]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)

    # Run code on startup of the worker process (optional)
    async def on_startup(ctx):
        os.makedirs(settings.REPORTS_DIR, exist_ok=True)
        logger.info(
            f"ARQ Worker started. Reports will be saved to '{settings.REPORTS_DIR}/'."
        )
