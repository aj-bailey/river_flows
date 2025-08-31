from river_flows.handlers.populate_oni_handler import PopulateONIHandler
from river_flows.repositories.oni_repository import ONIRepository

def test__populate_oni_handler_handle__all_years(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    repo = ONIRepository(session=session)
    handler = PopulateONIHandler(oni_repository=repo)
    year = None

    # Act
    result = handler.handle(year=year)
    
    # Assert
    assert result >= 1

def test__populate_oni_handler_handle__single_year(initialize_and_clean_db):
    # Arrange
    session = initialize_and_clean_db
    repo = ONIRepository(session=session)
    handler = PopulateONIHandler(oni_repository=repo)
    year = 1999

    # Act
    result = handler.handle(year=year)
    
    # Assert
    assert result == 1