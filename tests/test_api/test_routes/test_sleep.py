from unittest.mock import AsyncMock

from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_sleep():
    resp = client.get('/sleep')
    assert resp.status_code == 200
    assert resp.content.decode('utf-8') == '0'


def test_async_sleep_called(mocker):

    def create_async_mock(*args, **kwargs):
        am = AsyncMock(*args, **kwargs)
        return am()

    api_asyncio_mock = mocker.patch("fastapi_example.api.routes.sleep.asyncio")
    api_sleep_mock = api_asyncio_mock.sleep

    api_sleep_mock.side_effect = create_async_mock

    resp = client.get('/sleep?sleep_seconds=3')

    api_sleep_mock.assert_called()
    assert api_sleep_mock.call_count == 3
    assert resp.status_code == 200
    assert resp.content.decode('utf-8') == '3'
