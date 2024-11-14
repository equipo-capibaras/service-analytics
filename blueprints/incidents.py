from dataclasses import dataclass, field
from datetime import date
from typing import Any

import marshmallow_dataclass
from flask import Blueprint, Response, current_app, request
from flask.views import MethodView
from marshmallow import ValidationError

from .util import class_route, error_response, json_response, requires_token, validation_error_response

blp = Blueprint('Analytics Incidents', __name__)


mock_data = [
    {'date': '20170313', 'hour': '00', 'channel': 'Móvil', 'risk': 'Alto', 'escalations': 0},
    {'date': '20170314', 'hour': '01', 'channel': 'Móvil', 'risk': 'Alto', 'escalations': 0},
    {'date': '20170315', 'hour': '02', 'channel': 'Móvil', 'risk': 'Alto', 'escalations': 0},
    {'date': '20170316', 'hour': '03', 'channel': 'Web', 'risk': 'Alto', 'escalations': 0},
    {'date': '20170317', 'hour': '04', 'channel': 'Web', 'risk': 'Alto', 'escalations': 0},
    {'date': '20170318', 'hour': '05', 'channel': 'Móvil', 'risk': 'Alto', 'escalations': 0},
    {'date': '20170319', 'hour': '06', 'channel': 'Móvil', 'risk': 'Medio', 'escalations': 0},
    {'date': '20170313', 'hour': '07', 'channel': 'Correo', 'risk': 'Medio', 'escalations': 0},
    {'date': '20170314', 'hour': '08', 'channel': 'Correo', 'risk': 'Medio', 'escalations': 0},
    {'date': '20170315', 'hour': '09', 'channel': 'Móvil', 'risk': 'Medio', 'escalations': 1},
    {'date': '20170316', 'hour': '10', 'channel': 'Móvil', 'risk': 'Bajo', 'escalations': 1},
    {'date': '20170317', 'hour': '11', 'channel': 'Web', 'risk': 'Bajo', 'escalations': 1},
    {'date': '20170318', 'hour': '12', 'channel': 'Móvil', 'risk': 'Bajo', 'escalations': 1},
    {'date': '20170319', 'hour': '13', 'channel': 'Web', 'risk': 'Bajo', 'escalations': 1},
    {'date': '20170313', 'hour': '14', 'channel': 'Móvil', 'risk': 'Bajo', 'escalations': 1},
    {'date': '20170314', 'hour': '15', 'channel': 'Correo', 'risk': 'Bajo', 'escalations': 2},
    {'date': '20170315', 'hour': '16', 'channel': 'Móvil', 'risk': 'Bajo', 'escalations': 2},
    {'date': '20170316', 'hour': '17', 'channel': 'Móvil', 'risk': 'Bajo', 'escalations': 2},
    {'date': '20170317', 'hour': '18', 'channel': 'Web', 'risk': 'Bajo', 'escalations': 3},
    {'date': '20170318', 'hour': '19', 'channel': 'Web', 'risk': 'Bajo', 'escalations': 3},
    {'date': '20170319', 'hour': '20', 'channel': 'Correo', 'risk': 'Bajo', 'escalations': 3},
    {'date': '20170313', 'hour': '21', 'channel': 'Web', 'risk': 'Bajo', 'escalations': 4},
    {'date': '20170314', 'hour': '22', 'channel': 'Correo', 'risk': 'Bajo', 'escalations': 4},
    {'date': '20170315', 'hour': '23', 'channel': 'Móvil', 'risk': 'Bajo', 'escalations': 5},
]


@dataclass
class AnalyticsBody:
    startDate: date  # noqa: N815
    endDate: date  # noqa: N815
    fields: list[str] = field(default_factory=list)


@class_route(blp, '/api/v1/analytics/incidents')
class IncidentAnalytics(MethodView):
    init_every_request = False

    @requires_token
    def post(self, token: dict[str, Any]) -> Response:
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

        rows = [{'values': [row[field] for field in data.fields]} for row in mock_data]

        return json_response({'rows': rows}, 200)
