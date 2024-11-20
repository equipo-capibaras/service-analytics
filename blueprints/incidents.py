from dataclasses import dataclass, field
from datetime import date
from typing import Any

import marshmallow_dataclass
from dependency_injector.wiring import Provide
from flask import Blueprint, Response, current_app, request
from flask.views import MethodView
from marshmallow import ValidationError

from containers import Container
from repositories import IncidentAnalyticsRepository

from .util import class_route, error_response, json_response, requires_token, validation_error_response

blp = Blueprint('Analytics Incidents', __name__)


CHANNEL_I18N = {
    'es-CO': {
        'Email': 'Correo',
        'Web': 'Web',
        'Mobile': 'Móvil',
    },
    'es-AR': {
        'Email': 'Correo',
        'Web': 'Web',
        'Mobile': 'Móvil',
    },
    'pt-BR': {
        'Email': 'E-mail',
        'Web': 'Web',
        'Mobile': 'Celular',
    },
}

RISK_I18N = {
    'es-CO': {
        'Low': 'Bajo',
        'Medium': 'Medio',
        'High': 'Alto',
    },
    'es-AR': {
        'Low': 'Bajo',
        'Medium': 'Medio',
        'High': 'Alto',
    },
    'pt-BR': {
        'Low': 'Baixo',
        'Medium': 'Médio',
        'High': 'Alto',
    },
}


@dataclass
class AnalyticsBody:
    startDate: date  # noqa: N815
    endDate: date  # noqa: N815
    language: str
    fields: list[str] = field(default_factory=list)


class PopulateTableBody:
    entries: int


@class_route(blp, '/api/v1/analytics/<string:fact>')
class IncidentAnalytics(MethodView):
    init_every_request = False

    def fact_incidents(
        self, data: AnalyticsBody, incident_repo: IncidentAnalyticsRepository = Provide[Container.incidents_repo]
    ) -> list[dict[str, Any]]:
        # Get incidents from the repository based on the start and end dates
        incidents = incident_repo.get_incidents(start_date=data.startDate, end_date=data.endDate)

        for row in incidents:
            row['risk'] = RISK_I18N[data.language][row['risk']]
            row['channel'] = CHANNEL_I18N[data.language][row['channel']]

        return [{'values': [row[incident_field] for incident_field in data.fields]} for row in incidents]

    def fact_users(
        self, data: AnalyticsBody, incident_repo: IncidentAnalyticsRepository = Provide[Container.incidents_repo]
    ) -> list[dict[str, Any]]:
        users = incident_repo.get_users(start_date=data.startDate, end_date=data.endDate)

        for row in users:
            row['channel'] = CHANNEL_I18N[data.language][row['channel']]

        return [{'values': [row[field] for field in data.fields]} for row in users]

    @requires_token
    def post(
        self,
        token: dict[str, Any],
        fact: str,
    ) -> Response:
        client_schema = marshmallow_dataclass.class_schema(AnalyticsBody)()
        req_json = request.get_json(silent=True)

        if req_json is None:
            return error_response('The request body could not be parsed as valid JSON.', 400)

        # Validate request body
        try:
            data: AnalyticsBody = client_schema.load(req_json)
        except ValidationError as err:
            return validation_error_response(err)

        current_app.logger.info('Client: %s', token['cid'])

        if fact == 'incidents':
            rows = self.fact_incidents(data)
        elif fact == 'users':
            rows = self.fact_users(data)
        else:
            return error_response('Invalid fact', 400)

        return json_response({'rows': rows}, 200)


@class_route(blp, '/api/v1/analytics/incidents/populate')
class PopulateIncidents(MethodView):
    init_every_request = False

    def post(self, incident_repo: IncidentAnalyticsRepository = Provide[Container.incidents_repo]) -> Response:
        client_schema = marshmallow_dataclass.class_schema(PopulateTableBody)()
        req_json = request.get_json(silent=True)

        if req_json is None:
            return error_response('The request body could not be parsed as valid JSON.', 400)

        # Validate request body
        try:
            data: PopulateTableBody = client_schema.load(req_json)
        except ValidationError as err:
            return validation_error_response(err)

        incident_repo.populate_incidents(data.entries)

        return json_response({'message': 'Incidents populated successfully'}, 200)
