from river_flows.data.oni import ONI

from river_flows.repositories.oni_repository import ONIRepository

class ONIHandler():
    def __init__(self, oni_repository: ONIRepository):
        self.oni_repository = oni_repository
    
    def handle(self) -> list[ONI]:
        oni_data = self.oni_repository.get_records()

        return oni_data