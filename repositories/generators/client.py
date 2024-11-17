import secrets
from uuid import uuid4

from faker import Faker

from db import db
from models import Client
from models.enums import PlanEnum
from repositories import ClientRepository

from .utils import get_initial_final_date


class GeneratorClientRepository(ClientRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

    def populate_table(self, entries: int) -> None:
        clients = []

        dates = get_initial_final_date()

        for _ in range(entries):
            client = Client(
                id=str(uuid4()),
                name=self.faker.company(),
                plan=secrets.choice(
                    [
                        PlanEnum.EMPRESARIO.value,
                        PlanEnum.EMPRENDEDOR.value,
                        PlanEnum.EMPRESARIO_PLUS.value,
                    ]
                ),
                initial_date=dates['initial_date'],
                final_date=dates['final_date'],
            )
            clients.append(client)

        self.db.session.add_all(clients)
        self.db.session.commit()

    def get_random_client(self) -> Client:
        clients = self.db.session.query(Client).all()
        return secrets.choice(clients)

    def delete_all_clients(self) -> None:
        self.db.session.query(Client).delete()
        self.db.session.commit()
