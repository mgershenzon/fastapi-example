from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_bad_route():
    resp = client.get('/bad_route')
    assert resp.status_code == 500
    msg = """{"errors":["Internal server error: This error was expected as you called the 'bad_route' endpoint"]}"""
    assert resp.content.decode('utf-8') == msg


def test_http_404():
    resp = client.get('/http_404')
    assert resp.status_code == 404
    msg = """{"errors":["This is en example on how 404 error will look like"]}"""
    assert resp.content.decode('utf-8') == msg


def test_some_error_but_return_ok():
    resp = client.get('/some_error_but_return_ok')
    assert resp.status_code == 200
    msg = "OK"
    assert resp.content.decode('utf-8') == msg
