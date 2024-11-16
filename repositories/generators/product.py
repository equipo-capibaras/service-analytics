import secrets
from uuid import uuid4

from faker import Faker

from db import db
from models import Product
from models.enums import ProductTypeEnum
from repositories import ProductRepository


class GeneratorProductRepository(ProductRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

    def populate_table(self, entries: int) -> None:
        products = []

        for _ in range(entries):
            product = Product(
                id=str(uuid4()),
                name=self.faker.color_name(),
                type=secrets.choice(
                    [
                        ProductTypeEnum.HARDWARE.value,
                        ProductTypeEnum.SOFTWARE.value,
                        ProductTypeEnum.SERVICE.value,
                        ProductTypeEnum.OTHER.value,
                    ]
                ),
                description=self.faker.text(),
            )
            products.append(product)

        self.db.session.add_all(products)
        self.db.session.commit()

    def get_random_product(self) -> Product:
        products = self.db.session.query(Product).all()
        return secrets.choice(products)

    def delete_all_products(self) -> None:
        self.db.session.query(Product).delete()
        self.db.session.commit()
