from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import current_app
from app.utils.parse_workbook import parse_workbook_list

scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        current_app.logger.info("Scheduler started.")

        # Schedule the job to run every month on the 1st at 00:00
        scheduler.add_job(
            func=parse_workbook_list,
            trigger=CronTrigger(day=1, hour=0, minute=0),
            id="monthly_parser",
            replace_existing=True
        )

        current_app.logger.info("Monthly parser task scheduled.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        current_app.logger.info("Scheduler stopped.")
