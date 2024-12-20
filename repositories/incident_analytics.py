from datetime import date
from typing import Any

from models import IncidentAnalytics


class IncidentAnalyticsRepository:
    def clear_tables(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def populate_tables(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def reset(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def populate_incidents(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_incidents(self, client_id: str, start_date: date, end_date: date) -> list[dict[str, Any]]:
        raise NotImplementedError  # pragma: no cover

    def incident_to_dict(self, incident: IncidentAnalytics) -> dict[str, Any]:
        raise NotImplementedError  # pragma: no cover

    def user_to_dict(self, incident: IncidentAnalytics) -> dict[str, Any]:
        raise NotImplementedError  # pragma: no cover

    def get_users(self, client_id: str, start_date: date, end_date: date) -> list[dict[str, Any]]:
        raise NotImplementedError  # pragma: no cover

    def get_all(self, client_id: str, start_date: date, end_date: date) -> list[IncidentAnalytics]:
        raise NotImplementedError  # pragma: no cover
