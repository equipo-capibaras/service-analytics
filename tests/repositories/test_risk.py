from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import Risk
from repositories.generators import GeneratorRiskRepository


class TestRiskRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorRiskRepository()
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

        # Verificamos que haya 3 riesgos en la base de datos
        risks = db.session.query(Risk).all()
        self.assertEqual(len(risks), 3, f'Expected 3 risks, but found {len(risks)}')

    def test_get_random_risk(self) -> None:
        # Poblamos la tabla con 3 riesgos y probamos obtener uno aleatorio
        self.repository.populate_table()
        random_risk = self.repository.get_random_risk()

        # Comprobamos que el riesgo obtenido no sea None y que esté en la base de datos
        self.assertIsNotNone(random_risk, 'Expected a Risk object, but got None.')
        self.assertIsInstance(random_risk, Risk, 'Expected a Risk object, but got another type.')
        self.assertIsNotNone(Risk.query.get(random_risk.id), 'Risk does not exist in the database.')

    def test_delete_all_risks(self) -> None:
        # Poblamos la tabla con 3 riesgos
        self.repository.populate_table()

        # Eliminamos todos los riesgos
        self.repository.delete_all_risks()

        # Comprobamos que no haya riesgos en la base de datos
        risks_count = Risk.query.count()
        self.assertEqual(risks_count, 0, f'Expected 0 risks, but found {risks_count}')
