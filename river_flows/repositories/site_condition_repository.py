from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from river_flows.data.site_condition import BatchSiteConditions, SiteCondition
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

    def upsert_records(self, records: BatchSiteConditions) -> int:
        with self.session as session:
            for batch in records.batch_site_conditions:
                with session.begin():
                    site_condition_values = [
                        record.model_dump(exclude_unset=True) for record in batch
                    ]
                    insert_stmt = insert(SiteConditionORM).values(site_condition_values)
                    upsert_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=[
                            SiteConditionORM.site_id,
                            SiteConditionORM.timestamp,
                        ],
                        set_={
                            "site_name": insert_stmt.excluded.site_name,
                            "value": insert_stmt.excluded.value,
                            "unit": insert_stmt.excluded.unit,
                            "updated_at": insert_stmt.excluded.updated_at,
                        },
                    )

                    session.execute(upsert_stmt)

        upsert_count = len(records.site_conditions)

        return upsert_count

    def get_records(
        self, start_date: datetime, end_date: datetime, site_id: str
    ) -> list[SiteCondition]:
        with self.session as session:
            with session.begin():
                records = (
                    session.query(SiteConditionORM)
                    .filter(
                        SiteConditionORM.timestamp >= start_date,
                        SiteConditionORM.timestamp < end_date,
                        SiteConditionORM.site_id == site_id,
                    )
                    .all()
                )

            results = [SiteCondition.model_validate(record) for record in records]

        return results
