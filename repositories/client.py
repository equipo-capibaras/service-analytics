from models import Client


class ClientRepository:
    def populate_table(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_client(self) -> Client:
        raise NotImplementedError  # pragma: no cover

    def delete_all_clients(self) -> None:
        raise NotImplementedError  # pragma: no cover
