from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_info():
    resp = client.get('/info')
    assert resp.status_code == 200
