from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import Time
from repositories.generators import GeneratorTimeRepository


class TestTimeRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorTimeRepository()
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
        self.repository.populate_table()

        # Verificamos que haya 10 horas en la base de datos
        times = db.session.query(Time).all()
        self.assertEqual(len(times), 25, f'Expected 25 times, but found {len(times)}')

    def test_get_random_time(self) -> None:
        # Poblamos la tabla con 5 horas y probamos obtener una aleatoria
        self.repository.populate_table()
        random_time = self.repository.get_random_time()

        # Comprobamos que la hora obtenida no sea None y que esté en la base de datos
        self.assertIsNotNone(random_time, 'Expected a Time object, but got None.')
        self.assertIsInstance(random_time, Time, 'Expected a Time object, but got another type.')
        self.assertIsNotNone(Time.query.get(random_time.id), 'Time does not exist in the database.')

    def test_delete_all_times(self) -> None:
        # Poblamos la tabla con 5 horas
        self.repository.populate_table()

        # Eliminamos todas las horas
        self.repository.delete_all_times()

        # Comprobamos que no haya horas en la base de datos
        times_count = Time.query.count()
        self.assertEqual(times_count, 0, f'Expected 0 times, but found {times_count}')
