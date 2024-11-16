from models import Date


class DateRepository:
    def populate_table(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_date(self) -> Date:
        raise NotImplementedError  # pragma: no cover

    def delete_all_dates(self) -> None:
        raise NotImplementedError  # pragma: no cover
