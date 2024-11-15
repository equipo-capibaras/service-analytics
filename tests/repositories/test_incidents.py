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