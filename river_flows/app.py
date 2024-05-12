from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from river_flows.background_jobs.scheduler import schedule_jobs
from river_flows.clients.usgs_client import USGSClient
from river_flows.data.requests import PopulateSiteConditionsRequest
from river_flows.handlers.populate_site_conditions_handler import PopulateSiteConditionsHandler
from river_flows.repositories.site_condition_repository import SiteConditionRepository
from river_flows.utils.db import initialize_db, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    schedule_jobs()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {
        'result': 'GOOD'
    }


@app.post("/populate_site_conditions")
def populate_site_conditions(
        request_params: PopulateSiteConditionsRequest,
        session = Depends(get_session),
        ):
    site_id = request_params.site_id
    start_date = request_params.start_date
    end_date = request_params.end_date

    usgs_client = USGSClient(site=site_id)
    site_condition_repo = SiteConditionRepository(session)
    handler = PopulateSiteConditionsHandler(usgs_client=usgs_client, site_condition_repo=site_condition_repo)

    try:
        count_site_conditions_upserted = handler.handle(start_date=start_date, end_date=end_date)
    except Exception as e:
        return {"site_conditions_populated": False}

    return {"site_conditions_populated": True, "count_site_conditions_upserted": count_site_conditions_upserted}
