from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_get_is_alive():
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.content.decode('utf-8') == 'OK!'


def test_get_is_ready():
    resp = client.get('/is_ready')
    assert resp.status_code == 200
    assert resp.content.decode('utf-8') == 'OK!'
