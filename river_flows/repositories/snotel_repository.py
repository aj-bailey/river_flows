from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from river_flows.data.snotel import BatchSnotel, Snotel
from river_flows.orm.snotel import Snotel as SnotelORM
from river_flows.repositories.base import AbstractRepository


class SnotelRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_record(self, record: Snotel) -> Snotel:
        with self.session as session:
            snotel_record = SnotelORM(**record.model_dump())
            session.add(snotel_record)
            session.commit()
            inserted_snotel_record = Snotel.model_validate(snotel_record)

        return inserted_snotel_record

    def upsert_records(self, records: BatchSnotel) -> int:
        with self.session as session:
            for batch in records.batch_snotel:
                with session.begin():
                    snotel_data = [
                        record.model_dump(exclude_unset=True) for record in batch
                    ]
                    insert_stmt = insert(SnotelORM).values(snotel_data)
                    upsert_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=[
                            SnotelORM.station_triplets,
                            SnotelORM.timestamp,
                        ],
                        set_={
                            "prec": insert_stmt.excluded.prec,
                            "tobs": insert_stmt.excluded.tobs,
                            "wteq": insert_stmt.excluded.wteq,
                            "snwd": insert_stmt.excluded.snwd,
                            "updated_at": insert_stmt.excluded.updated_at,
                        },
                    )

                    session.execute(upsert_stmt)

        upsert_count = len(records.snotel_data)

        return upsert_count

    def get_records(
        self, start_date: datetime, end_date: datetime, station_triplets: str
    ) -> list[Snotel]:
        with self.session as session:
            with session.begin():
                records = (
                    session.query(SnotelORM)
                    .filter(
                        SnotelORM.timestamp >= start_date,
                        SnotelORM.timestamp < end_date,
                        SnotelORM.station_triplets == station_triplets,
                    )
                    .all()
                )

            results = [Snotel.model_validate(record) for record in records]

        return results
