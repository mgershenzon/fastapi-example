from unittest.mock import PropertyMock

import pytest
import uvicorn

from fastapi_example.config import Config


def raise_sys_exit(*_args, **_kwargs):
    raise SystemExit(99)


def test_main(mocker):
    uvicorn_mock = mocker.patch.object(uvicorn, "run")

    import fastapi_example.main

    fastapi_example.main.main()
    uvicorn_mock.assert_any_call('main:app', host='0.0.0.0', port=80, log_config=Config.LOGGING_CONFIG,
                                 workers=fastapi_example.main.Config.WORKERS)


def test_sys_exit(mocker):
    mocker.patch.object(uvicorn, "run", side_effect=raise_sys_exit)

    with pytest.raises(RuntimeError) as e:
        import fastapi_example.main
        fastapi_example.main.main()

    msg = "Problem with uvicorn. Exit code: '99'"

    assert e.value.args[0] == msg


def test_get_application():
    from fastapi_example import main
    a = main.get_application()
    middleware_funcs = [m.kwargs['dispatch'].__name__ for m in a.user_middleware if 'dispatch' in m.kwargs]
    assert "add_useful_headers" in middleware_funcs
    assert "add_try_except" in middleware_funcs


# This test is here to see that no one deletes the profiler requirement by mistake
def test_profiler(mocker):
    from fastapi_example import main

    mocker.patch("fastapi_example.config.Config.PROFILING_ON", return_value=True, new_callable=PropertyMock)

    a = main.get_application()
    middleware_clss = str([str(m.cls) for m in a.user_middleware])

    assert "PyInstrumentProfilerMiddleware" in middleware_clss
