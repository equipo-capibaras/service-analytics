import datetime
from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import Date
from repositories.generators import GeneratorDateRepository


class TestDateRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorDateRepository()
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
        start_date = datetime.date(2024, 9, 1)
        end_date = start_date + datetime.timedelta(days=9)

        # Poblamos la tabla con 10 entradas
        self.repository.populate_table(start_date, end_date)

        # Verificamos que haya 10 fechas en la base de datos
        dates = db.session.query(Date).all()
        self.assertEqual(len(dates), 10, f'Expected 10 dates, but found {len(dates)}')

    def test_get_random_date(self) -> None:
        start_date = datetime.date(2024, 9, 1)
        end_date = start_date + datetime.timedelta(days=4)

        # Poblamos la tabla con 5 fechas y probamos obtener una aleatoria
        self.repository.populate_table(start_date, end_date)
        random_date = self.repository.get_random_date()

        # Comprobamos que la fecha obtenida no sea None y que esté en la base de datos
        self.assertIsNotNone(random_date, 'Expected a Date object, but got None.')
        self.assertIsInstance(random_date, Date, 'Expected a Date object, but got another type.')
        self.assertIsNotNone(Date.query.get(random_date.id), 'Date does not exist in the database.')

    def test_delete_all_dates(self) -> None:
        start_date = datetime.date(2024, 9, 1)
        end_date = start_date + datetime.timedelta(days=4)

        # Poblamos la tabla con 5 fechas
        self.repository.populate_table(start_date, end_date)

        # Eliminamos todas las fechas
        self.repository.delete_all_dates()

        # Comprobamos que no haya fechas en la base de datos
        dates_count = Date.query.count()
        self.assertEqual(dates_count, 0, f'Expected 0 dates, but found {dates_count}')
