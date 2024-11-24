import datetime
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

    def populate_table(self, start_date: datetime.date, end_date: datetime.date) -> None:
        dates = []

        num_days = (end_date - start_date).days + 1

        for i in range(num_days):
            generated_date = start_date + datetime.timedelta(days=i)
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
