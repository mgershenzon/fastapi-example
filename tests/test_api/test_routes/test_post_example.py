from starlette.testclient import TestClient

from fastapi_example.main import app

client = TestClient(app)


def test_post():
    resp = client.post('/post_example', json={"str_for_example": "t_e_s_t__p_o_s_t", "float_or_none_for_example": 3.0})
    assert resp.status_code == 200
    assert resp.content.decode('utf-8') == '{"str_for_example":"t_e_s_t__p_o_s_t","float_or_none_for_example":3.0}'


def test_post_no_float():
    resp = client.post('/post_example', json={"str_for_example": "t_e_s_t__p_o_s_t"})
    assert resp.status_code == 200
    assert resp.content.decode('utf-8') == '{"str_for_example":"t_e_s_t__p_o_s_t","float_or_none_for_example":null}'


def test_fails_on_missing_param():
    resp = client.post('/post_example', json={})
    assert resp.status_code == 422

    # we split the expected message, so that it won't include the pydentic version
    # example: https://errors.pydantic.dev/2.1/v/missing

    in_msg1 = '{"detail":[{"type":"missing","loc":["body","str_for_example"],"msg":"Field required","input":{},'
    in_msg2 = '"url":"https://errors.pydantic.dev'
    in_msg3 = '/v/missing"}]}'
    assert in_msg1 in resp.content.decode('utf-8')
    assert in_msg2 in resp.content.decode('utf-8')
    assert in_msg3 in resp.content.decode('utf-8')
