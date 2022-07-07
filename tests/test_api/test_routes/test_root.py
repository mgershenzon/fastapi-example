from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_root():
    resp = client.get('/')
    assert resp.status_code == 200
