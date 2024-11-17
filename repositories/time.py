from models import Time


class TimeRepository:
    def populate_table(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_time(self) -> Time:
        raise NotImplementedError  # pragma: no cover

    def delete_all_times(self) -> None:
        raise NotImplementedError  # pragma: no cover
