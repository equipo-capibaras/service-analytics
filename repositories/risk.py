from models import Risk


class RiskRepository:
    def populate_table(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_risk(self) -> Risk:
        raise NotImplementedError  # pragma: no cover

    def delete_all_risks(self) -> None:
        raise NotImplementedError  # pragma: no cover
