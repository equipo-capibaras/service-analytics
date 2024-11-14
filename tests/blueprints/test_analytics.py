import base64
import json
from typing import Any, cast

from faker import Faker
from unittest_parametrize import ParametrizedTestCase, parametrize
from werkzeug.test import TestResponse

from app import create_app


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

    def call_incidents_api(self, body: dict[str, Any] | str, token: dict[str, str] | None) -> TestResponse:
        token_encoded = base64.urlsafe_b64encode(json.dumps(token).encode()).decode() if token is not None else None

        headers = {'X-Apigateway-Api-Userinfo': token_encoded} if token_encoded is not None else {}

        return self.client.post(
            '/api/v1/analytics/incidents',
            data=body if isinstance(body, str) else json.dumps(body),
            content_type='application/json',
            headers=headers,
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
            'fields': ['hour', 'channel', 'risk'],
        }
        resp = self.call_incidents_api(body, token=token)

        self.assertEqual(resp.status_code, 400)
        resp_data = json.loads(resp.get_data())

        self.assertEqual(resp_data['code'], 400)
        self.assertEqual(resp_data['message'], 'Invalid value for startDate: Not a valid date.')

    def test_analytics(self) -> None:
        token = self.gen_token_client(client_id=cast(str, self.faker.uuid4()), role='admin')

        body = {
            'startDate': '2017-03-13',
            'endDate': '2017-03-19',
            'fields': ['hour', 'channel', 'risk'],
        }

        resp = self.call_incidents_api(body, token=token)

        self.assertEqual(resp.status_code, 200)
