from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from river_flows.background_jobs.save_previous_date_river_flows import (
    save_previous_date_river_flows,
)


def schedule_jobs():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(save_previous_date_river_flows, CronTrigger(hour=8))
    print("Added save_previous_date_river_flows background job")

    scheduler.start()
