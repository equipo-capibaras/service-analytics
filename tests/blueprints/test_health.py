from unittest import TestCase

from app import create_app


class TestHealth(TestCase):
    def setUp(self) -> None:
        app = create_app(database_uri='sqlite:///:memory:')
        self.client = app.test_client()

        self.app_ctx = app.app_context()
        self.app_ctx.push()

    def tearDown(self) -> None:
        self.app_ctx.pop()
        del self.app_ctx

    def test_health(self) -> None:
        resp = self.client.get('/api/v1/health/analytics')

        self.assertEqual(resp.status_code, 200)
