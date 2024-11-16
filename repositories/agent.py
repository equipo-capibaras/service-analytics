from models import Agent


class AgentRepository:
    def populate_table(self, entries: int) -> None:
        raise NotImplementedError  # pragma: no cover

    def get_random_agent(self) -> Agent:
        raise NotImplementedError  # pragma: no cover

    def delete_all_agents(self) -> None:
        raise NotImplementedError  # pragma: no cover
