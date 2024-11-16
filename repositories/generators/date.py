import secrets
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

        for _ in range(entries):
            date = Date(
                id=str(uuid4()),
                date=self.faker.date_this_decade(),
                day=self.faker.day_of_month(),
                month=self.faker.month(),
                quarter=self.faker.random_int(min=1, max=4),
                year=self.faker.year(),
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
