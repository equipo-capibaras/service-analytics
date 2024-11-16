from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import Agent
from repositories.generators import GeneratorAgentRepository


class TestAgentRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorAgentRepository()
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

        # Verificamos que haya 10 agentes en la base de datos
        agents = db.session.query(Agent).all()
        self.assertEqual(len(agents), 10, f'Expected 10 agents, but found {len(agents)}')

    def test_get_random_agent(self) -> None:
        # Poblamos la tabla con 5 agentes y probamos obtener uno aleatorio
        self.repository.populate_table(5)
        random_agent = self.repository.get_random_agent()

        # Comprobamos que el agente obtenido no sea None y que esté en la base de datos
        self.assertIsNotNone(random_agent, 'Expected an Agent object, but got None.')
        self.assertIsInstance(random_agent, Agent, 'Expected an Agent object, but got another type.')
        self.assertIsNotNone(Agent.query.get(random_agent.id), 'Agent does not exist in the database.')

    def test_delete_all_agents(self) -> None:
        # Poblamos la tabla con 5 agentes
        self.repository.populate_table(5)

        # Eliminamos todos los agentes
        self.repository.delete_all_agents()

        # Comprobamos que no haya agentes en la base de datos
        agents_count = Agent.query.count()
        self.assertEqual(agents_count, 0, f'Expected 0 agents, but found {agents_count}')
