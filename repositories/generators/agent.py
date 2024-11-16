import secrets
from uuid import uuid4

from faker import Faker

from db import db
from models import Agent
from repositories import AgentRepository


class GeneratorAgentRepository(AgentRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

    def populate_table(self, entries: int) -> None:
        agents = []

        for _ in range(entries):
            agent = Agent(
                id=str(uuid4()),
                name=self.faker.name(),
                experience=self.faker.random_int(min=1, max=30),
            )
            agents.append(agent)

        self.db.session.add_all(agents)
        self.db.session.commit()

    def get_random_agent(self) -> Agent:
        agents = self.db.session.query(Agent).all()
        return secrets.choice(agents)

    def delete_all_agents(self) -> None:
        self.db.session.query(Agent).delete()
        self.db.session.commit()
