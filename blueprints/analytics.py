from typing import Any

from dependency_injector.wiring import Provide
from flask import Blueprint, Response
from flask.views import MethodView

from containers import Container
from models import Role
from repositories import IncidentAnalyticsRepository

from .util import class_route, error_response, json_response, requires_token

blp = Blueprint('Analytics', __name__)


@class_route(blp, '/api/v1/analytics/incidents/results')
class Analytics(MethodView):
    init_every_request = False

    @requires_token
    def get(
        self, token: dict[str, Any], incident_repo: IncidentAnalyticsRepository = Provide[Container.incidents_repo]
    ) -> Response:
        if token['role'] != Role.ADMIN.value:
            return error_response('Forbidden: You do not have access to this resource.', 403)

        incidents = incident_repo.get_incidents()
        if not incidents:
            return error_response('No incidents found, please populate the tables', 404)

        list_incidents = [incident_repo.incident_to_dict(incident) for incident in incidents]

        return json_response(list_incidents, 200)
