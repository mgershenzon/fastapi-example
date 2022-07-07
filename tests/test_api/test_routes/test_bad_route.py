from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_bad_route():
    resp = client.get('/bad_route')
    assert resp.status_code == 500
    msg = """{"errors":["Internal server error: This error was expected as you called the 'bad_route' endpoint"]}"""
    assert resp.content.decode('utf-8') == msg
