import secrets
from datetime import UTC, datetime
from uuid import uuid4

from faker import Faker

from db import db
from models import Date
from models.enums import DayOfWeekEnum


class GeneratorDateRepository:
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

    def populate_table(self, entries: int) -> None:
        dates = []

        start_date = datetime(2024, 9, 1, tzinfo=UTC)
        end_date = datetime(2024, 11, 30, tzinfo=UTC)

        for _ in range(entries):
            generated_date = self.faker.date_between(start_date=start_date, end_date=end_date)
            date = Date(
                id=str(uuid4()),
                date=generated_date,
                day=str(generated_date.day).zfill(2),
                month=str(generated_date.month).zfill(2),
                quarter=(generated_date.month - 1) // 3 + 1,
                year=str(generated_date.year),
                day_of_week=secrets.choice(
                    [
                        DayOfWeekEnum.MONDAY.value,
                        DayOfWeekEnum.TUESDAY.value,
                        DayOfWeekEnum.WEDNESDAY.value,
                        DayOfWeekEnum.THURSDAY.value,
                        DayOfWeekEnum.FRIDAY.value,
                        DayOfWeekEnum.SATURDAY.value,
                        DayOfWeekEnum.SUNDAY.value,
                    ]
                ),
            )
            dates.append(date)

        self.db.session.add_all(dates)
        self.db.session.commit()

    def get_random_date(self) -> Date:
        dates = self.db.session.query(Date).all()
        return secrets.choice(dates)

    def delete_all_dates(self) -> None:
        self.db.session.query(Date).delete()
        self.db.session.commit()
