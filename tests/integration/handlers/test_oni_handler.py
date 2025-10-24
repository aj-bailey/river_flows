from river_flows.data.oni import ONI
from river_flows.handlers.oni_handler import ONIHandler
from river_flows.repositories.oni_repository import ONIRepository


def test__oni_handler__success(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    oni_repository = ONIRepository(session=session)
    handler = ONIHandler(oni_repository=oni_repository)

    # Act
    oni_data = handler.handle()

    # Assert
    assert isinstance(oni_data, list)
    assert all(isinstance(od, ONI) for od in oni_data)
