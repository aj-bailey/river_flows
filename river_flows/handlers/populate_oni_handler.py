from river_flows.data.oni import ONI, BatchONI
from river_flows.repositories.oni_repository import ONIRepository
from river_flows.utils.oni_scaper import ONIScraper

class PopulateONIHandler():
    def __init__(self, oni_repository: ONIRepository):
        self.oni_repository = oni_repository
        self.oni_scraper = ONIScraper()

    def handle(self, year: int | None = None ) -> int:
        oni_df = self.oni_scraper.scrape_oni_data()

        if year:
            records = oni_df[oni_df['year'] == year].to_dict(orient="records")
        else:
            records = oni_df.to_dict(orient="records")

        oni_data = [ONI.model_validate(record) for record in records]
        batch_oni = BatchONI(oni_data=oni_data)

        upserted_record_count = self.oni_repository.upsert_records(records=batch_oni)

        return upserted_record_count
