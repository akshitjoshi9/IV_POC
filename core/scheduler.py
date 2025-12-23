import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError
from loguru import logger

from core.tasks import web_scrapping_task

scheduler = BackgroundScheduler()

def async_task_wrapper():
    try:
        asyncio.run(web_scrapping_task())
    except Exception as e:
        logger.error(f"Error running scheduled async task: {e}")

def start_scheduler():
    try:
        scheduler.remove_job("web-scrapping-task")
    except JobLookupError:
        pass

    scheduler.add_job(
        func=async_task_wrapper,
        trigger=CronTrigger(hour=9, minute=0),
        id="web-scrapping-task",
        name="Runs every Morning at 9 AM",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Scheduler started with job: web-scrapping-task")
