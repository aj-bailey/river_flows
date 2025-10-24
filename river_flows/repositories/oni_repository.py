
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from river_flows.data.oni import BatchONI, ONI
from river_flows.orm.oni import ONI as OniORM
from river_flows.repositories.base import AbstractRepository


class ONIRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def upsert_records(self, records: BatchONI) -> int:
        with self.session as session:
            for batch in records.batch_oni:
                with session.begin():
                    oni_data = [
                        record.model_dump(exclude_unset=True) for record in batch
                    ]
                    insert_stmt = insert(OniORM).values(oni_data)
                    upsert_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=[
                            OniORM.year,
                        ],
                        set_={
                            "djf": insert_stmt.excluded.djf,
                            "jfm": insert_stmt.excluded.jfm,
                            "fma": insert_stmt.excluded.fma,
                            "mam": insert_stmt.excluded.mam,
                            "amj": insert_stmt.excluded.amj,
                            "mjj": insert_stmt.excluded.mjj,
                            "jja": insert_stmt.excluded.jja,
                            "jas": insert_stmt.excluded.jas,
                            "aso": insert_stmt.excluded.aso,
                            "son": insert_stmt.excluded.son,
                            "ond": insert_stmt.excluded.ond,
                            "ndj": insert_stmt.excluded.ndj,
                            "updated_at": insert_stmt.excluded.updated_at,
                        },
                    )

                    session.execute(upsert_stmt)

        upsert_count = len(records.oni_data)

        return upsert_count

    def get_records(self) -> list[ONI]:
        with self.session as session:
            with session.begin():
                records = session.query(OniORM).all()
            results = [ONI.model_validate(record) for record in records]

        return results
