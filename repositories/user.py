from models import User


class UserRepository:
    def populate_table(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_user(self) -> User:
        raise NotImplementedError  # pragma: no cover

    def delete_all_users(self) -> None:
        raise NotImplementedError  # pragma: no cover
