from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import Client
from repositories.generators import GeneratorClientRepository


class TestClientRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorClientRepository()
        self.faker = Faker()
        self.client = app.test_client()
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self) -> None:
        # Eliminar el contexto de la aplicación
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def test_populate_table(self) -> None:
        # Poblamos la tabla con 10 entradas
        self.repository.populate_table(10)

        # Verificamos que haya 10 clientes en la base de datos
        clients = db.session.query(Client).all()
        self.assertEqual(len(clients), 10, f'Expected 10 clients, but found {len(clients)}')

    def test_get_random_client(self) -> None:
        # Poblamos la tabla con 5 clientes y probamos obtener uno aleatorio
        self.repository.populate_table(5)
        random_client = self.repository.get_random_client()

        # Comprobamos que el cliente obtenido no sea None y que esté en la base de datos
        self.assertIsNotNone(random_client, 'Expected a Client object, but got None.')
        self.assertIsInstance(random_client, Client, 'Expected a Client object, but got another type.')
        self.assertIsNotNone(Client.query.get(random_client.id), 'Client does not exist in the database.')

    def test_delete_all_clients(self) -> None:
        # Poblamos la tabla con 5 clientes
        self.repository.populate_table(5)

        # Eliminamos todos los clientes
        self.repository.delete_all_clients()

        # Comprobamos que no haya clientes en la base de datos
        clients_count = Client.query.count()
        self.assertEqual(clients_count, 0, f'Expected 0 clients, but found {clients_count}')
