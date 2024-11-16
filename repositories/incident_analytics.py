from typing import Any

from models import IncidentAnalytics


class IncidentAnalyticsRepository:
    def clear_tables(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def populate_tables(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def populate_incidents(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_incidents(self) -> list[dict[str, Any]]:
        raise NotImplementedError  # pragma: no cover

    def incident_to_dict(self, incident: IncidentAnalytics) -> dict[str, Any]:
        raise NotImplementedError  # pragma: no cover
