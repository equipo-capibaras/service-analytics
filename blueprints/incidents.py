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

mock_data = [
    {
        'userId': '162e35e7-f058-498c-a475-72a49daf72ee',
        'age': '20-29',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Correo',
        'product': 'Internet hogar',
        'satisfaction': 7.2,
    },
    {
        'userId': '162e35e7-f058-498c-a475-72a49daf72ee',
        'age': '20-29',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Web',
        'product': 'TV',
        'satisfaction': 6.4,
    },
    {
        'userId': '162e35e7-f058-498c-a475-72a49daf72ee',
        'age': '20-29',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Móvil',
        'product': 'Celular',
        'satisfaction': 7.8,
    },
    {
        'userId': 'df493fc9-4244-471e-b6b1-fc8b057fca50',
        'age': '20-29',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Móvil',
        'product': 'Celular',
        'satisfaction': 5.2,
    },
    {
        'userId': '8c24ece3-a48c-4046-b509-d628793566e8',
        'age': '20-29',
        'language': 'Español (Argentina)',
        'country': 'Argentina',
        'channel': 'Móvil',
        'product': 'TV',
        'satisfaction': 8.3,
    },
    {
        'userId': '51a20874-b7de-45eb-bf0b-d0698606e709',
        'age': '20-29',
        'language': 'Español (Argentina)',
        'country': 'Argentina',
        'channel': 'Móvil',
        'product': 'TV',
        'satisfaction': 6.7,
    },
    {
        'userId': '91669e2f-0c74-4633-b543-6ccdf89e485a',
        'age': '20-29',
        'language': 'Español (Argentina)',
        'country': 'Argentina',
        'channel': 'Web',
        'product': 'Internet hogar',
        'satisfaction': 2.1,
    },
    {
        'userId': 'db1cd9a3-4116-43ff-a2e1-ef1b53b035a9',
        'age': '20-29',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Web',
        'product': 'Internet hogar',
        'satisfaction': 9.8,
    },
    {
        'userId': '251b0367-dacb-44ed-a918-5998358a4dff',
        'age': '20-29',
        'language': 'Portugués (Brasil)',
        'country': 'Brasil',
        'channel': 'Web',
        'product': 'Celular',
        'satisfaction': 3.2,
    },
    {
        'userId': '23ce4ace-0408-4139-b314-ef77392c1590',
        'age': '30-39',
        'language': 'Portugués (Brasil)',
        'country': 'Brasil',
        'channel': 'Web',
        'product': 'Celular',
        'satisfaction': 4.6,
    },
    {
        'userId': '8fea847a-8793-4640-811e-d7df0244fa0f',
        'age': '30-39',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Correo',
        'product': 'TV',
        'satisfaction': 8.6,
    },
    {
        'userId': 'b08d9a1d-0a92-48d7-a68d-2fd9a3a07673',
        'age': '30-39',
        'language': 'Portugués (Brasil)',
        'country': 'Brasil',
        'channel': 'Correo',
        'product': 'TV',
        'satisfaction': 7.0,
    },
    {
        'userId': '9a1ada5f-6051-4742-b760-6c50813622b9',
        'age': '30-39',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Correo',
        'product': 'Celular',
        'satisfaction': 4.3,
    },
    {
        'userId': '5fee8961-2644-4299-b3d9-62000c64a351',
        'age': '30-39',
        'language': 'Portugués (Brasil)',
        'country': 'Brasil',
        'channel': 'Web',
        'product': 'Celular',
        'satisfaction': 6.7,
    },
    {
        'userId': '58636075-4873-49c3-b369-15a0a385104c',
        'age': '30-39',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Web',
        'product': 'TV',
        'satisfaction': 2.9,
    },
    {
        'userId': 'e2d9a94d-53e9-4452-b328-080de802c582',
        'age': '40-49',
        'language': 'Portugués (Brasil)',
        'country': 'Brasil',
        'channel': 'Web',
        'product': 'TV',
        'satisfaction': 9.0,
    },
    {
        'userId': '97a4532d-86cf-43aa-954f-620831f09b06',
        'age': '40-49',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Web',
        'product': 'Internet hogar',
        'satisfaction': 6.2,
    },
    {
        'userId': 'fd103046-c77f-416e-beb0-a3ac2ad68450',
        'age': '40-49',
        'language': 'Español (Argentina)',
        'country': 'Argentina',
        'channel': 'Móvil',
        'product': 'Internet hogar',
        'satisfaction': 5.5,
    },
    {
        'userId': '6c04fbcb-0466-4712-8bc5-888f3b0a723c',
        'age': '40-49',
        'language': 'Español (Argentina)',
        'country': 'Argentina',
        'channel': 'Móvil',
        'product': 'Internet hogar',
        'satisfaction': 2.3,
    },
    {
        'userId': '45bd1ac2-22da-4dd1-9d88-fda1e0dee658',
        'age': '50-59',
        'language': 'Portugués (Brasil)',
        'country': 'Brasil',
        'channel': 'Móvil',
        'product': 'TV',
        'satisfaction': 4.7,
    },
    {
        'userId': '271d2319-c484-449e-81fe-2a3d7d870879',
        'age': '50-59',
        'language': 'Español (Argentina)',
        'country': 'Argentina',
        'channel': 'Móvil',
        'product': 'TV',
        'satisfaction': 5.8,
    },
    {
        'userId': '65fe43c8-20c2-4087-8dfc-6d01788772b0',
        'age': '50-59',
        'language': 'Español (Argentina)',
        'country': 'Argentina',
        'channel': 'Móvil',
        'product': 'Internet hogar',
        'satisfaction': 6.2,
    },
    {
        'userId': '713f9011-c9aa-4cae-ad8b-a4eb639353a3',
        'age': '60-69',
        'language': 'Portugués (Brasil)',
        'country': 'Brasil',
        'channel': 'Móvil',
        'product': 'Celular',
        'satisfaction': 7.7,
    },
    {
        'userId': '740dc203-736f-4b4f-839a-454f95ded610',
        'age': '60-69',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Móvil',
        'product': 'Celular',
        'satisfaction': 8.9,
    },
    {
        'userId': '32ead394-a8fc-4cac-9d5b-ea4a3d336ec9',
        'age': '70+',
        'language': 'Español (Colombia)',
        'country': 'Colombia',
        'channel': 'Web',
        'product': 'Celular',
        'satisfaction': 5.5,
    },
]


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

    def fact_users(self, data: AnalyticsBody) -> list[dict[str, Any]]:
        return [{'values': [row[field] for field in data.fields]} for row in mock_data]

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
