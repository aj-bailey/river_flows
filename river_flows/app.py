from contextlib import asynccontextmanager
from datetime import date

from fastapi import Depends, FastAPI

from river_flows.background_jobs.scheduler import schedule_jobs
from river_flows.clients.usgs_client import USGSClient
from river_flows.clients.snotel_client import SnotelAPIClient
from river_flows.data.requests import (
    GetSiteConditionsRequest,
    GetSnotelRequest,
    PopulateHourlyRiverFlowFeaturesRequest,
    PopulateONIRequest,
    PopulateSiteConditionsRequest,
    PopulateSnotelRequest,
)
from river_flows.data.responses import (
    ONIResponse,
    SiteConditionsResponse,
    SnotelResponse,
)
from river_flows.handlers.populate_hourly_river_flow_features_handler import (
    PopulateHourlyRiverFlowFeaturesHandler,
)
from river_flows.handlers.populate_oni_handler import PopulateONIHandler
from river_flows.handlers.populate_site_conditions_handler import (
    PopulateSiteConditionsHandler,
)
from river_flows.handlers.oni_handler import ONIHandler
from river_flows.handlers.populate_snotel_handler import PopulateSnotelHandler
from river_flows.handlers.site_conditions_handler import SiteConditionsHandler
from river_flows.handlers.snotel_handler import SnotelHandler
from river_flows.repositories.hourly_river_flow_features_repository import (
    HourlyRiverFlowFeaturesRepository,
)
from river_flows.repositories.oni_repository import ONIRepository
from river_flows.repositories.site_condition_repository import SiteConditionRepository
from river_flows.repositories.snotel_repository import SnotelRepository
from river_flows.utils.db import (
    initialize_db,
    get_session,
    get_multi_transaction_session,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    # schedule_jobs()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"result": "GOOD"}


@app.post("/populate_site_conditions")
def populate_site_conditions(
    request_params: PopulateSiteConditionsRequest,
    session=Depends(get_session),
):
    site_id = request_params.site_id
    start_date = request_params.start_date
    end_date = request_params.end_date

    usgs_client = USGSClient(site=site_id)
    site_condition_repo = SiteConditionRepository(session)
    handler = PopulateSiteConditionsHandler(
        usgs_client=usgs_client, site_condition_repo=site_condition_repo
    )

    try:
        count_site_conditions_upserted = handler.handle(
            start_date=start_date, end_date=end_date
        )
    except Exception as e:
        return {"site_conditions_populated": False}

    return {
        "site_conditions_populated": True,
        "count_site_conditions_upserted": count_site_conditions_upserted,
    }


@app.get("/site_conditions")  # TODO: refactor /site_conditions/{site_id}/
def site_conditions(
    request_params: GetSiteConditionsRequest = Depends(),
    session=Depends(get_session),
):
    site_id = request_params.site_id
    start_date = request_params.start_date
    end_date = request_params.end_date

    site_condition_repo = SiteConditionRepository(session)
    handler = SiteConditionsHandler(site_condition_repo=site_condition_repo)

    try:
        site_conditions = handler.handle(
            start_date=start_date, end_date=end_date, site_id=site_id
        )
    except Exception as e:
        return SiteConditionsResponse(result="failure", error=str(e))

    return SiteConditionsResponse(result="success", data=site_conditions)


@app.post("/populate_snotel")
def populate_snotel_year(
    request_params: PopulateSnotelRequest,
    session=Depends(get_session),
):
    year = request_params.year
    station_triplets = request_params.station_triplets

    snotel_repo = SnotelRepository(session)
    snotel_client = SnotelAPIClient()
    handler = PopulateSnotelHandler(
        snotel_client=snotel_client, snotel_repository=snotel_repo
    )

    try:
        count_snotel_upserted = handler.handle(
            year=year, station_triplets=station_triplets
        )
    except Exception as e:
        return {"site_conditions_populated": False}

    return {
        "site_conditions_populated": True,
        "count_site_conditions_upserted": count_snotel_upserted,
    }


@app.get("/snotel")
def snotel(
    request_params: GetSnotelRequest = Depends(),
    session=Depends(get_session),
):
    start_date = request_params.start_date
    end_date = request_params.end_date
    station_triplets = request_params.station_triplets

    snotel_repo = SnotelRepository(session)
    handler = SnotelHandler(snotel_repo=snotel_repo)

    try:
        snotel_data = handler.handle(
            start_date=start_date, end_date=end_date, station_triplets=station_triplets
        )
    except Exception as e:
        return SnotelResponse(result="failure", error=str(e))

    return SnotelResponse(result="success", data=snotel_data)


@app.post("/populate_oni")
def populate_oni(
    request_params: PopulateONIRequest,
    session=Depends(get_session),
):
    year = request_params.year

    oni_repository = ONIRepository(session)
    handler = PopulateONIHandler(oni_repository=oni_repository)

    try:
        count_snotel_upserted = handler.handle(year=year)
    except Exception as e:
        return {"oni_populated": False}

    return {
        "oni_populated": True,
        "count_oni_populated": count_snotel_upserted,
    }


@app.get("/oni")
def oni(session=Depends(get_session)):
    oni_repository = ONIRepository(session)
    handler = ONIHandler(oni_repository=oni_repository)

    try:
        oni_data = handler.handle()
    except Exception as e:
        return ONIResponse(result="failure", error=str(e))

    return ONIResponse(result="success", data=oni_data)


@app.post("/populate_hourly_river_flow_features")
def populate_hourly_river_flow_features(
    request_params: PopulateHourlyRiverFlowFeaturesRequest,
    session=Depends(get_multi_transaction_session),
):
    oni_repository = ONIRepository(session)
    snotel_repository = SnotelRepository(session)
    site_condition_repository = SiteConditionRepository(session)
    hourly_river_flow_features_repository = HourlyRiverFlowFeaturesRepository(session)

    handler = PopulateHourlyRiverFlowFeaturesHandler(
        oni_repository=oni_repository,
        site_condition_repository=site_condition_repository,
        snotel_repository=snotel_repository,
        hourly_river_flow_features_repository=hourly_river_flow_features_repository,
    )

    try:
        count_features_upserted = handler.handle(request_params=request_params)
    except Exception as e:
        return {"hourly_river_flow_features_populated": False, "error": str(e)}

    return {
        "hourly_river_flow_features_populated": True,
        "count_features_populated": count_features_upserted,
    }
