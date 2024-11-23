import copy
import secrets

from faker import Faker

from db import db
from demo import client_list
from models import Client
from repositories import ClientRepository


class GeneratorClientRepository(ClientRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

    def populate_table(self) -> None:
        clients = [copy.deepcopy(client) for client in client_list]

        self.db.session.add_all(clients)
        self.db.session.commit()

    def get_random_client(self) -> Client:
        clients = self.db.session.query(Client).all()
        return secrets.choice(clients)

    def delete_all_clients(self) -> None:
        self.db.session.query(Client).delete()
        self.db.session.commit()
