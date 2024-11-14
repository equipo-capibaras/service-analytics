import secrets
from uuid import uuid4

from faker import Faker

from db import db
from models import Time
from repositories import TimeRepository

from .utils import count_time, get_random_time


class GeneratorTimeRepository(TimeRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

    def populate_table(self) -> None:
        times = []
        for _ in range(count_time()):
            reference_time = get_random_time()

            time = Time(
                id=str(uuid4()),
                hour=reference_time['hour'],
                minute=reference_time['minute'],
                part_of_day=reference_time['part_of_day'],
            )
            times.append(time)

        self.db.session.add_all(times)
        self.db.session.commit()

    def get_random_time(self) -> Time:
        times = self.db.session.query(Time).all()
        return secrets.choice(times)

    def delete_all_times(self) -> None:
        self.db.session.query(Time).delete()
        self.db.session.commit()
