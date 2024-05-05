import os

from sqlalchemy import text
from sqlalchemy.orm import Session


def clean_database(session: Session) -> None:
    if os.getenv('APP_ENV', None) == 'test':
        with session:
            sql = text("TRUNCATE TABLE inventories RESTART IDENTITY CASCADE;")
            session.execute(sql)
            session.commit()
