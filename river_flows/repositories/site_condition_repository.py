class SiteConditionRepository():
    pass

from sqlalchemy.orm import Session

from river_flows.data.site_condition import SiteCondition
from river_flows.orm.site_condition import SiteCondition as SiteConditionORM
from river_flows.repositories.base import AbstractRepository


class SiteConditionRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_record(self, record: SiteCondition) -> SiteCondition:
        with self.session as session:
            site_condition = SiteConditionORM(**record.model_dump())
            session.add(site_condition)
            session.commit()
            inserted_site_condition = SiteCondition.model_validate(site_condition)

        return inserted_site_condition
