from unittest import TestCase

from faker import Faker

from app import create_app
from db import db
from models import Product
from repositories.generators import GeneratorProductRepository


class TestProductRepository(TestCase):
    def setUp(self) -> None:
        # Configurar el contexto de la aplicación
        app = create_app(database_uri='sqlite:///:memory:')
        self.app = app
        self.repository = GeneratorProductRepository()
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

        # Verificamos que haya 10 productos en la base de datos
        products = db.session.query(Product).all()
        self.assertEqual(len(products), 10, f'Expected 10 products, but found {len(products)}')

    def test_get_random_product(self) -> None:
        # Poblamos la tabla con 5 productos y probamos obtener uno aleatorio
        self.repository.populate_table(5)
        random_product = self.repository.get_random_product()

        # Comprobamos que el producto obtenido no sea None y que esté en la base de datos
        self.assertIsNotNone(random_product, 'Expected a Product object, but got None.')
        self.assertIsInstance(random_product, Product, 'Expected a Product object, but got another type.')
        self.assertIsNotNone(Product.query.get(random_product.id), 'Product does not exist in the database.')

    def test_delete_all_products(self) -> None:
        # Poblamos la tabla con 5 productos
        self.repository.populate_table(5)

        # Eliminamos todos los productos
        self.repository.delete_all_products()

        # Comprobamos que no haya productos en la base de datos
        products_count = Product.query.count()
        self.assertEqual(products_count, 0, f'Expected 0 products, but found {products_count}')
