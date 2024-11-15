from typing import Any
from uuid import uuid4

from faker import Faker

from db import db
from models import IncidentAnalytics
from repositories import IncidentAnalyticsRepository

from .agent import GeneratorAgentRepository
from .channel import GeneratorChannelRepository
from .client import GeneratorClientRepository
from .date import GeneratorDateRepository
from .product import GeneratorProductRepository
from .risk import GeneratorRiskRepository
from .time import GeneratorTimeRepository
from .user import GeneratorUserRepository


class GeneratorIncidentAnalyticsRepository(IncidentAnalyticsRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db
        self.agent_repo = GeneratorAgentRepository()
        self.client_repo = GeneratorClientRepository()
        self.date_repo = GeneratorDateRepository()
        self.product_repo = GeneratorProductRepository()
        self.risk_repo = GeneratorRiskRepository()
        self.time_repo = GeneratorTimeRepository()
        self.user_repo = GeneratorUserRepository()
        self.channel_repo = GeneratorChannelRepository()
        self.TOTAL_AGENTS = 20
        self.TOTAL_CLIENTS = 10
        self.TOTAL_DATES = 10
        self.TOTAL_PRODUCTS = 10
        self.TOTAL_USERS = 400

    def populate_tables(self, entries: int) -> None:
        self.agent_repo.populate_table(self.TOTAL_AGENTS)
        self.client_repo.populate_table(self.TOTAL_CLIENTS)
        self.date_repo.populate_table(entries)
        self.product_repo.populate_table(self.TOTAL_PRODUCTS)
        self.risk_repo.populate_table()
        self.time_repo.populate_table()
        self.user_repo.populate_table(self.TOTAL_USERS)
        self.channel_repo.populate_table()

    def delete_all_incident_analytics(self) -> None:
        self.db.session.query(IncidentAnalytics).delete()
        self.db.session.commit()

    def clear_tables(self) -> None:
        self.delete_all_incident_analytics()
        self.agent_repo.delete_all_agents()
        self.client_repo.delete_all_clients()
        self.date_repo.delete_all_dates()
        self.product_repo.delete_all_products()
        self.risk_repo.delete_all_risks()
        self.time_repo.delete_all_times()
        self.user_repo.delete_all_users()
        self.channel_repo.delete_all_channels()

    def populate_incidents(self, entries: int) -> None:
        self.clear_tables()
        self.populate_tables(entries)

        incidents = []

        for _ in range(entries):
            user = self.user_repo.get_random_user()
            client = self.client_repo.get_random_client()
            product = self.product_repo.get_random_product()
            date = self.date_repo.get_random_date()
            time = self.time_repo.get_random_time()
            risk = self.risk_repo.get_random_risk()
            agent = self.agent_repo.get_random_agent()
            channel = self.channel_repo.get_random_channel()

            incident = IncidentAnalytics(
                id=str(uuid4()),
                user_name=user.name,
                user_age=user.age,
                user_city=user.city,
                user_country=user.country,
                user_continent=user.continent,
                user_language=user.language,
                client_name=client.name,
                client_plan=client.plan.value,
                product_name=product.name,
                product_type=product.type.value,
                product_description=product.description,
                date_day=date.day,
                date_month=date.month,
                date_quarter=date.quarter,
                date_year=date.year,
                date_day_of_week=date.day_of_week.value,
                time_hour=time.hour,
                time_minute=time.minute,
                time_part_of_day=time.part_of_day,
                risk_level=risk.risk_level.value,
                agent_name=agent.name,
                agent_experience=agent.experience,
                channel_type=channel.channel_type.value,
                scaling_level=self.faker.random_int(min=1, max=10),
                resolution_time=self.faker.random_int(min=1, max=100),
            )
            incidents.append(incident)

        self.db.session.add_all(incidents)
        self.db.session.commit()

    def get_incidents(self) -> list[IncidentAnalytics]:
        return self.db.session.query(IncidentAnalytics).all()

    def incident_to_dict(self, incident: IncidentAnalytics) -> dict[str, Any]:
        return {
            'id': incident.id,
            'user_name': incident.user_name,
            'user_age': incident.user_age,
            'user_city': incident.user_city,
            'user_country': incident.user_country,
            'user_continent': incident.user_continent,
            'user_language': incident.user_language,
            'client_name': incident.client_name,
            'client_plan': incident.client_plan,
            'product_name': incident.product_name,
            'product_type': incident.product_type,
            'product_description': incident.product_description,
            'date_day': incident.date_day,
            'date_month': incident.date_month,
            'date_quarter': incident.date_quarter,
            'date_year': incident.date_year,
            'date_day_of_week': incident.date_day_of_week,
            'time_hour': incident.time_hour,
            'time_minute': incident.time_minute,
            'time_part_of_day': incident.time_part_of_day,
            'risk_level': incident.risk_level,
            'agent_name': incident.agent_name,
            'agent_experience': incident.agent_experience,
            'channel_type': incident.channel_type,
            'scaling_level': incident.scaling_level,
            'resolution_time': incident.resolution_time,
        }
