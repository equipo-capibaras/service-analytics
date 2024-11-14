from models import Product


class ProductRepository:
    def populate_table(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_product(self) -> Product:
        raise NotImplementedError  # pragma: no cover

    def delete_all_products(self) -> None:
        raise NotImplementedError  # pragma: no cover
