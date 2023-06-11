from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_bad_route():
    resp = client.get('/bad_route')
    assert resp.status_code == 500
    msg = """{"errors":["Internal server error: This error was expected as you called the 'bad_route' endpoint"]}"""
    assert resp.content.decode('utf-8') == msg


def test_http_404_example():
    resp = client.get('/http_404')
    assert resp.status_code == 404

    msg = ('{"errors":["Url \'http://testserver/http_404\' not found, details: \'This is '
           'an example of how a 404 error will look like\'"]}')

    assert resp.content.decode('utf-8') == msg


def test_http_404():
    resp = client.get('/there_is_no_such_route_in_the_code_only_in_tests')
    assert resp.status_code == 404

    msg = ('{"errors":["Url '
           "'http://testserver/there_is_no_such_route_in_the_code_only_in_tests' not "
           'found, details: \'Not Found\'"]}')

    assert resp.content.decode('utf-8') == msg


def test_some_error_but_return_ok():
    resp = client.get('/some_error_but_return_ok')
    assert resp.status_code == 200
    msg = "OK"
    assert resp.content.decode('utf-8') == msg


def test_bad_request_error_for_odd_numbers_happy():
    resp = client.get('/bad_request_error_for_odd_numbers/2')
    assert resp.status_code == 200
    msg = "2"
    assert resp.content.decode('utf-8') == msg


def test_bad_request_error_for_odd_numbers_sad():
    resp = client.get('/bad_request_error_for_odd_numbers/1')
    assert resp.status_code == 418
    msg = """{"errors":["Odd numbers get this error"]}"""
    assert resp.content.decode('utf-8') == msg
