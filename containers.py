from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from repositories.generators import GeneratorIncidentAnalyticsRepository


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=['blueprints'])
    config = providers.Configuration()

    incidents_repo = providers.ThreadSafeSingleton(GeneratorIncidentAnalyticsRepository)
