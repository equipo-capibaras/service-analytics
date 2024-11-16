from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import User
from repositories.generators import GeneratorUserRepository


class TestUserRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorUserRepository()
        self.faker = Faker()
        self.client = app.test_client()
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self) -> None:
        # Eliminar el contexto de la aplicación
        db.session.remove()  # Asegura que no queden sesiones abiertas
        db.drop_all()
        self.app_ctx.pop()

    def test_populate_table(self) -> None:
        # Poblamos la tabla con 10 entradas
        self.repository.populate_table(10)

        # Verificamos que haya 10 usuarios en la base de datos
        users = db.session.query(User).all()
        self.assertEqual(len(users), 10, f'Expected 10 users, but found {len(users)}')

    def test_get_random_user(self) -> None:
        # Poblamos la tabla con 5 usuarios y probamos obtener uno aleatorio
        self.repository.populate_table(5)
        random_user = self.repository.get_random_user()

        # Comprobamos que el usuario obtenido no sea None y que esté en la base de datos
        self.assertIsNotNone(random_user, 'Expected a User object, but got None.')
        self.assertIsInstance(random_user, User, 'Expected a User object, but got another type.')
        self.assertIsNotNone(User.query.get(random_user.id), 'User does not exist in the database.')

    def test_delete_all_users(self) -> None:
        # Poblamos la tabla con 5 usuarios
        self.repository.populate_table(5)

        # Eliminamos todos los usuarios
        self.repository.delete_all_users()

        # Comprobamos que no haya usuarios en la base de datos
        users_count = User.query.count()
        self.assertEqual(users_count, 0, f'Expected 0 users, but found {users_count}')
