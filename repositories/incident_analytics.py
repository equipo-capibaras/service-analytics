from models import IncidentAnalytics


class IncidentAnalyticsRepository:
    def clear_tables(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def populate_tables(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def populate_incidents(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_incidents(self) -> list[IncidentAnalytics]:
        raise NotImplementedError  # pragma: no cover
