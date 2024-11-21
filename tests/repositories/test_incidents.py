from datetime import date
from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import IncidentAnalytics
from repositories.generators import GeneratorIncidentAnalyticsRepository


class TestIncidentAnalyticsRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorIncidentAnalyticsRepository()
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

    def test_populate_tables(self) -> None:
        # Poblamos las tablas con 10 entradas
        self.repository.populate_incidents(10)

        # Verificamos que haya 10 entradas en la tabla de IncidentAnalytics
        incidents = db.session.query(IncidentAnalytics).all()

        self.assertEqual(len(incidents), 10, f'Expected 10 incidents, but found {len(incidents)}')

    def test_delete_all_incident_analytics(self) -> None:
        # Poblamos las tablas con 10 entradas
        self.repository.populate_tables(10)

        # Eliminamos todas las entradas
        self.repository.delete_all_incident_analytics()

        # Comprobamos que no haya entradas en la tabla de IncidentAnalytics
        incidents_count = IncidentAnalytics.query.count()
        self.assertEqual(incidents_count, 0, f'Expected 0 incidents, but found {incidents_count}')

    def test_get_all_incidents_in_date_range(self) -> None:
        # Poblamos las tablas con 10 entradas
        self.repository.populate_incidents(10)

        # Definimos un rango de fechas para buscar los incidentes
        start_date = date(2024, 9, 1)
        end_date = date(2024, 11, 30)

        # Obtenemos los incidentes en el rango de fechas
        incidents = self.repository.get_all(start_date, end_date)

        # Comprobamos que se devuelvan 10 incidentes
        self.assertEqual(len(incidents), 10, f'Expected 10 incidents in date range, but found {len(incidents)}')

    def test_get_incidents_filtered(self) -> None:
        # Poblamos las tablas con 10 entradas
        self.repository.populate_incidents(10)

        # Definimos un rango de fechas para buscar los incidentes
        start_date = date(2024, 9, 1)
        end_date = date(2024, 11, 30)

        # Obtenemos los incidentes en el rango de fechas
        incidents = self.repository.get_incidents(start_date, end_date)

        # Comprobamos que se devuelvan 10 incidentes como diccionarios
        self.assertEqual(len(incidents), 10, f'Expected 10 incidents in date range, but found {len(incidents)}')
        self.assertIsInstance(incidents[0], dict, 'Expected incident to be a dictionary')

    def test_get_users_filtered(self) -> None:
        # Poblamos las tablas con 10 entradas
        self.repository.populate_incidents(10)

        # Definimos un rango de fechas para buscar los usuarios
        start_date = date(2024, 9, 1)
        end_date = date(2024, 11, 30)

        # Obtenemos los usuarios en el rango de fechas
        users = self.repository.get_users(start_date, end_date)

        # Comprobamos que se devuelvan 10 usuarios como diccionarios
        self.assertEqual(len(users), 10, f'Expected 10 users in date range, but found {len(users)}')
        self.assertIsInstance(users[0], dict, 'Expected user to be a dictionary')
        self.assertIn('userId', users[0], 'Expected user dictionary to contain userId key')

    def test_clear_tables(self) -> None:
        # Poblamos las tablas con 10 entradas
        self.repository.populate_incidents(10)

        # Limpiamos todas las tablas
        self.repository.clear_tables()

        # Comprobamos que no haya entradas en la tabla de IncidentAnalytics
        incidents_count = IncidentAnalytics.query.count()
        self.assertEqual(incidents_count, 0, f'Expected 0 incidents after clearing tables, but found {incidents_count}')
