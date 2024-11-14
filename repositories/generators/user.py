import secrets
from uuid import uuid4

from faker import Faker

from db import db
from models import User
from repositories import UserRepository

from .utils import get_random_languaje, get_random_sex, get_random_ubication


class GeneratorUserRepository(UserRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

    def populate_table(self, entries: int) -> None:
        users = []
        for _ in range(entries):
            ubication = get_random_ubication()
            user = User(
                id=str(uuid4()),
                name=self.faker.name(),
                age=self.faker.random_int(min=18, max=99),
                sex=get_random_sex(),
                city=ubication['city'],
                country=ubication['country'],
                continent=ubication['continent'],
                language=get_random_languaje(),
                initial_date=self.faker.date_between_dates(
                    date_start=self.faker.date_this_decade(before_today=True),
                    date_end=self.faker.date_this_decade(before_today=True),
                ),
                final_date=self.faker.date_between_dates(
                    date_start=self.faker.date_this_decade(before_today=False),
                    date_end=self.faker.date_this_decade(before_today=False),
                ),
            )
            users.append(user)

        self.db.session.add_all(users)
        self.db.session.commit()

    def get_random_user(self) -> User:
        users = self.db.session.query(User).all()
        return secrets.choice(users)

    def delete_all_users(self) -> None:
        self.db.session.query(User).delete()
        self.db.session.commit()
