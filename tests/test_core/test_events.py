from unittest.mock import MagicMock

from starlette.testclient import TestClient

from fastapi_example.core import events
from fastapi_example.main import app


def test_create_stop_start_app_handlers():
    info_mock = MagicMock()
    events.logger.info = info_mock

    with TestClient(app) as client:
        client.get("/health")
        assert info_mock.call_count == 1

    assert info_mock.call_count == 2
