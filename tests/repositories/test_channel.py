from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import  Channel
from repositories.generators import GeneratorChannelRepository

class TestChannelRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorChannelRepository()
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
        # Poblamos la tabla con 3 entradas
        self.repository.populate_table()

        # Verificamos que haya 3 canales en la base de datos
        channels = db.session.query(Channel).all()
        self.assertEqual(len(channels), 3, f'Expected 3 channels, but found {len(channels)}')

    def test_get_random_channel(self) -> None:
        # Poblamos la tabla con 3 canales y probamos obtener uno aleatorio
        self.repository.populate_table()
        random_channel = self.repository.get_random_channel()

        # Comprobamos que el canal obtenido no sea None y que esté en la base de datos
        self.assertIsNotNone(random_channel, 'Expected a Channel object, but got None.')
        self.assertIsInstance(random_channel, Channel, 'Expected a Channel object, but got another type.')
        self.assertIsNotNone(Channel.query.get(random_channel.id), 'Channel does not exist in the database.')

    def test_delete_all_channels(self) -> None:
        # Poblamos la tabla con 3 canales
        self.repository.populate_table()

        # Eliminamos todos los canales
        self.repository.delete_all_channels()

        # Comprobamos que no haya canales en la base de datos
        channels_count = Channel.query.count()
        self.assertEqual(channels_count, 0, f'Expected 0 channels, but found {channels_count}')