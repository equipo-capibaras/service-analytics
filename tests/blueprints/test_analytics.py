import base64
import json
from typing import Any, cast
from unittest.mock import Mock

from faker import Faker
from unittest_parametrize import ParametrizedTestCase, parametrize
from werkzeug.test import TestResponse

from app import create_app
from repositories import IncidentAnalyticsRepository


class TestIncidents(ParametrizedTestCase):
    def setUp(self) -> None:
        self.faker = Faker()

        self.app = create_app(database_uri='sqlite:///:memory:')
        self.client = self.app.test_client()

    def gen_token_client(self, *, client_id: str | None, role: str) -> dict[str, Any]:
        return {
            'sub': cast(str, self.faker.uuid4()),
            'cid': client_id,
            'role': role,
            'aud': 'analytics',
        }

    def call_fact_api(self, fact: str, body: dict[str, Any] | str, token: dict[str, str] | None) -> TestResponse:
        token_encoded = base64.urlsafe_b64encode(json.dumps(token).encode()).decode() if token is not None else None

        headers = {'X-Apigateway-Api-Userinfo': token_encoded} if token_encoded is not None else {}

        return self.client.post(
            f'/api/v1/analytics/{fact}',
            data=body if isinstance(body, str) else json.dumps(body),
            content_type='application/json',
            headers=headers,
        )

    def call_incidents_api(self, body: dict[str, Any] | str, token: dict[str, str] | None) -> TestResponse:
        return self.call_fact_api('incidents', body, token)

    def call_users_api(self, body: dict[str, Any] | str, token: dict[str, str] | None) -> TestResponse:
        return self.call_fact_api('users', body, token)

    def call_populate_api(self, body: dict[str, Any] | str) -> TestResponse:
        return self.client.post(
            '/api/v1/analytics/incidents/populate',
            data=body if isinstance(body, str) else json.dumps(body),
            content_type='application/json',
        )

    def call_reset_api(self) -> TestResponse:
        return self.client.post(
            '/api/v1/reset/analytics',
            data='{}',
            content_type='application/json',
        )

    @parametrize(
        'missing_field',
        [
            ('sub',),
            ('cid',),
            ('role',),
            ('aud',),
        ],
    )
    def test_info_token_missing_fields(self, missing_field: str) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')
        del token[missing_field]

        body = {
            'startDate': '2017-03-13',
            'endDate': '2017-03-19',
            'language': 'es-CO',
            'fields': ['hour', 'channel', 'risk'],
        }
        resp = self.call_incidents_api(body, token=token)

        self.assertEqual(resp.status_code, 401)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data, {'code': 401, 'message': f'{missing_field} is missing in token'})

    def test_analytics_invalid_json(self) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')

        body = 'invalid json'
        resp = self.call_incidents_api(body, token=token)

        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['code'], 400)
        self.assertEqual(resp_data['message'], 'The request body could not be parsed as valid JSON.')

    def test_analytics_missing_token(self) -> None:
        body = {
            'startDate': '2017-03-13',
            'endDate': '2017-03-19',
            'language': 'es-CO',
            'fields': ['hour', 'channel', 'risk'],
        }
        resp = self.call_incidents_api(body, token=None)

        self.assertEqual(resp.status_code, 401)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['code'], 401)
        self.assertEqual(resp_data['message'], 'Token is missing')

    def test_analytics_invalid_data(self) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')

        body = {
            'startDate': self.faker.pystr(),
            'endDate': '2017-03-19',
            'language': 'es-CO',
            'fields': ['hour', 'channel', 'risk'],
        }
        resp = self.call_incidents_api(body, token=token)

        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['code'], 400)
        self.assertEqual(resp_data['message'], 'Invalid value for startDate: Not a valid date.')

    def test_analytics_invalid_fact(self) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')

        body = {
            'startDate': '2023-03-19',
            'endDate': '2023-03-19',
            'language': 'es-AR',
            'fields': ['foo', 'bar'],
        }
        resp = self.call_fact_api('doesNotExist', body, token=token)

        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['code'], 400)
        self.assertEqual(resp_data['message'], 'Invalid fact')

    def test_analytics_incidents(self) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')
        fields = ['hour', 'channel', 'risk']
        body = {
            'startDate': '2017-03-13',
            'endDate': '2017-03-19',
            'language': 'es-CO',
            'fields': fields,
        }

        mock_data = [
            {
                'date': '20170313',
                'hour': '00',
                'channel': 'Email',
                'risk': 'Low',
                'escalations': 0,
                'resolution_time': 1800.0 / 3600.0,
                'product_name': 'Internet hogar',
                'agent_name': 'Julian Cordoba Rincón',
            },
            {
                'date': '20170314',
                'hour': '01',
                'channel': 'Web',
                'risk': 'Medium',
                'escalations': 0,
                'resolution_time': 26800.0 / 3600.0,
                'product_name': 'Internet hogar',
                'agent_name': 'Julian Cordoba Rincón',
            },
            {
                'date': '20170314',
                'hour': '01',
                'channel': 'Mobile',
                'risk': 'High',
                'escalations': 0,
                'resolution_time': 26800.0 / 3600.0,
                'product_name': 'Internet hogar',
                'agent_name': 'Julian Cordoba Rincón',
            },
        ]

        analytics_repo_mock = Mock(IncidentAnalyticsRepository)
        cast(Mock, analytics_repo_mock.get_incidents).return_value = mock_data
        with self.app.container.incidents_repo.override(analytics_repo_mock):
            resp = self.call_incidents_api(body, token=token)

        self.assertEqual(resp.status_code, 200)

    def test_analytics_users(self) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')
        fields = ['age', 'channel', 'satisfaction']
        body = {
            'startDate': '2024-03-13',
            'endDate': '2024-03-19',
            'language': 'es-CO',
            'fields': fields,
        }

        resp = self.call_users_api(body, token=token)

        self.assertEqual(resp.status_code, 200)

    def test_analytics_no_incidents(self) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')
        body = {
            'startDate': '2017-03-13',
            'endDate': '2017-03-19',
            'language': 'es-CO',
            'fields': ['hour', 'channel', 'risk'],
        }

        analytics_repo_mock = Mock(IncidentAnalyticsRepository)
        cast(Mock, analytics_repo_mock.get_incidents).return_value = []
        with self.app.container.incidents_repo.override(analytics_repo_mock):
            resp = self.call_incidents_api(body, token=token)

        self.assertEqual(resp.status_code, 200)

    def test_populate_invalid_json(self) -> None:
        body = 'invalid json'
        resp = self.call_populate_api(body)

        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['code'], 400)
        self.assertEqual(resp_data['message'], 'The request body could not be parsed as valid JSON.')

    def test_populate_incidents(self) -> None:
        body = {'entries': 10}

        analytics_repo_mock = Mock(IncidentAnalyticsRepository)
        with self.app.container.incidents_repo.override(analytics_repo_mock):
            resp = self.call_populate_api(body)

        cast(Mock, analytics_repo_mock.populate_incidents).assert_called_once_with(10)

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['message'], 'Incidents populated successfully')

    def test_reset(self) -> None:
        analytics_repo_mock = Mock(IncidentAnalyticsRepository)
        with self.app.container.incidents_repo.override(analytics_repo_mock):
            resp = self.call_reset_api()

        cast(Mock, analytics_repo_mock.reset).assert_called_once()

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['status'], 'Ok')
