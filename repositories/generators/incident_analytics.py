from datetime import date
from typing import Any
from uuid import uuid4

from faker import Faker
from sqlalchemy import and_

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
from .utils import get_random_age_range


class GeneratorIncidentAnalyticsRepository(IncidentAnalyticsRepository):
    def __init__(self) -> None:
        self.faker = Faker()
        self.db = db

        # Repositorios necesarios para obtener datos de entidades relacionadas
        self.agent_repo = GeneratorAgentRepository()
        self.client_repo = GeneratorClientRepository()
        self.date_repo = GeneratorDateRepository()
        self.product_repo = GeneratorProductRepository()
        self.risk_repo = GeneratorRiskRepository()
        self.time_repo = GeneratorTimeRepository()
        self.user_repo = GeneratorUserRepository()
        self.channel_repo = GeneratorChannelRepository()

        # Configuración para el número de entidades a generar
        self.TOTAL_AGENTS = 20
        self.TOTAL_CLIENTS = 10
        self.TOTAL_PRODUCTS = 10
        self.TOTAL_USERS = 400

    def populate_tables(self, entries: int) -> None:
        # Llenar las tablas de referencia
        self.agent_repo.populate_table(self.TOTAL_AGENTS)
        self.client_repo.populate_table(self.TOTAL_CLIENTS)
        self.product_repo.populate_table(self.TOTAL_PRODUCTS)
        self.user_repo.populate_table(self.TOTAL_USERS)
        self.date_repo.populate_table(entries)
        self.risk_repo.populate_table()
        self.time_repo.populate_table()
        self.channel_repo.populate_table()

    def delete_all_incident_analytics(self) -> None:
        # Eliminar todos los registros de incidentes analíticos
        self.db.session.query(IncidentAnalytics).delete()
        self.db.session.commit()

    def clear_tables(self) -> None:
        # Limpiar todos los datos de las tablas
        self.delete_all_incident_analytics()
        self.agent_repo.delete_all_agents()
        self.client_repo.delete_all_clients()
        self.product_repo.delete_all_products()
        self.user_repo.delete_all_users()
        self.date_repo.delete_all_dates()
        self.risk_repo.delete_all_risks()
        self.time_repo.delete_all_times()
        self.channel_repo.delete_all_channels()

    def populate_incidents(self, entries: int) -> None:
        # Llenar los incidentes analíticos
        self.clear_tables()
        self.populate_tables(entries)

        incidents = []

        for _ in range(entries):
            # Obtener datos aleatorios para los incidentes
            user = self.user_repo.get_random_user()
            client = self.client_repo.get_random_client()
            product = self.product_repo.get_random_product()
            date_object = self.date_repo.get_random_date()
            time = self.time_repo.get_random_time()
            risk = self.risk_repo.get_random_risk()
            agent = self.agent_repo.get_random_agent()
            channel = self.channel_repo.get_random_channel()

            # Crear un nuevo incidente analítico
            incident = IncidentAnalytics(
                id=str(uuid4()),
                user_id=user.id,
                user_name=user.name,
                user_age=user.age,
                user_age_range=get_random_age_range(),
                user_city=user.city,
                user_country=user.country,
                user_continent=user.continent,
                user_language=user.language,
                client_name=client.name,
                client_plan=client.plan.value,
                product_name=product.name,
                product_type=product.type.value,
                product_description=product.description,
                date=date_object.date,
                date_day=date_object.day,
                date_month=date_object.month,
                date_quarter=date_object.quarter,
                date_year=date_object.year,
                date_day_of_week=date_object.day_of_week.value,
                time_hour=time.hour,
                time_minute=time.minute,
                time_part_of_day=time.part_of_day,
                risk_level=risk.risk_level.value,
                agent_name=agent.name,
                agent_experience=agent.experience,
                channel_type=channel.channel_type.value,
                scaling_level=self.faker.random_int(min=1, max=10),
                resolution_time=self.faker.random_int(min=1, max=30),
                satisfaction=self.faker.random_int(min=1, max=10),
            )
            incidents.append(incident)

        # Agregar todos los incidentes generados a la base de datos
        self.db.session.add_all(incidents)
        self.db.session.commit()

    def get_all(self, start_date: date, end_date: date) -> list[IncidentAnalytics]:
        # Filtrar los incidentes según el rango de fechas usando comparaciones directas
        return (
            self.db.session.query(IncidentAnalytics)
            .filter(
                and_(
                    IncidentAnalytics.date >= start_date,
                    IncidentAnalytics.date <= end_date,
                )
            )
            .all()
        )

    def get_incidents(self, start_date: date, end_date: date) -> list[dict[str, Any]]:
        # Filtrar los incidentes según el rango de fechas usando comparaciones directas
        incidents = self.get_all(start_date, end_date)

        return [self.incident_to_dict(incident) for incident in incidents]

    def get_users(self, start_date: date, end_date: date) -> list[dict[str, Any]]:
        # Filtrar los usuarios según el rango de fechas usando comparaciones directas
        users = self.get_all(start_date, end_date)

        return [self.user_to_dict(user) for user in users]

    def incident_to_dict(self, incident: IncidentAnalytics) -> dict[str, Any]:
        # Convertir un incidente a un formato de diccionario
        return {
            'date': incident.date_year + incident.date_month.zfill(2) + incident.date_day.zfill(2),
            'hour': str(incident.time_hour).zfill(2),
            'channel': incident.channel_type,
            'risk': incident.risk_level,
            'escalations': incident.scaling_level,
            'resolution_time': incident.resolution_time,
            'product_name': incident.product_name,
            'agent_name': incident.agent_name,
        }

    def user_to_dict(self, incident: IncidentAnalytics) -> dict[str, Any]:
        # convertir un usuario a un formato de diccionario
        return {
            'userId': incident.user_id,
            'age': incident.user_age_range,
            'language': incident.user_language,
            'country': incident.user_country,
            'channel': incident.channel_type,
            'product': incident.product_name,
            'satisfaction': round(float(incident.satisfaction), 1),
        }
