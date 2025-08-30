from abc import ABC

from sqlalchemy.orm import Session

from river_flows.data.responses import ModelType


class AbstractRepository(ABC):
    def __init__(self, session: Session):
        self.session = session

    def create_record(self, record: ModelType) -> ModelType:
        pass

    # def get_record_by_id(self, record_id: int) -> ModelType:
    #     pass

    # def update_record(self, record: ModelType) -> ModelType:
    #     pass

    # def delete_record(self, record_id: int) -> ModelType:
    #     pass
