import json
import re
import sys
from json import JSONDecodeError
from logging import LogRecord

import pytest

import fastapi_example.logging.custom_formatter as custom_formatter

FIELD_LIST = ['asctime', 'levelname', 'message']
ADDITIONAL_DEBUG_FIELDS = ['pathname', 'lineno', 'threadName', 'thread']
EXTRA_FIELDS_MAP = {'compid': 'fastapi_example-test111'}

STACK_INFO_FOR_TEST = """
Stack (most recent call last):
  File "<string>", line 1, in <module>
  File "/python3.7/multiprocessing/spawn.py", line 105, in spawn_main
    exitcode = _main(fd)
  File "/python3.7/multiprocessing/spawn.py", line 118, in _main
    return self._bootstrap()
  File "/python3.7/multiprocessing/process.py", line 297, in _bootstrap
    self.run()
  File "/python3.7/multiprocessing/process.py", line 99, in run
    self._target(*self._args, **self._kwargs)
  File "/FORTESTS/venv/lib/python3.7/site-packages/uvicorn/subprocess.py", line 76, in subprocess_started
    target(sockets=sockets)
  File "/FORTESTS/venv/lib/python3.7/site-packages/uvicorn/server.py", line 50, in run
    loop.run_until_complete(self.serve(sockets=sockets))
  File "/python3.7/asyncio/base_events.py", line 574, in run_until_complete
    self.run_forever()
  File "/python3.7/asyncio/base_events.py", line 541, in run_forever
    self._run_once()
  File "/python3.7/asyncio/base_events.py", line 1786, in _run_once
    handle._run()
  File "/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "/FORTESTS/venv/lib/python3.7/site-packages/starlette/middleware/base.py", line 38, in coro
    await self.app(scope, receive, send)
  File "/FORTESTS/venv/lib/python3.7/site-packages/starlette/middleware/base.py", line 25, in __call__
    response = await self.dispatch_func(request, self.call_next)
  File "/FORTESTS/fastapi_example/api/middlewares/try_except_middleware.py", line 15, in add_try_except
    logger.exception(msg, stack_info=True)
"""


def test_custom_json_formatter_with_stack_info(mocker):
    mocker.patch("fastapi_example.config.Config.JSON_LOG_FORMAT", new=True)

    formatter = custom_formatter.CustomFormatter(
        '%(asctime)s %(compid)s %(levelname)-7s %(correlation_id)-36s %(message)s',
        EXTRA_FIELDS_MAP
    )

    err_msg = 'Internal server error: division by zero'
    log_rec_with_stack_info = LogRecord("test", 40, "test", 999, err_msg, (),
                                        sys.exc_info(), 'add_try_except', STACK_INFO_FOR_TEST)
    res = formatter.format(log_rec_with_stack_info)
    assert err_msg in res
    assert 'fastapi_example/api/middlewares/try_except_middleware.py' in res
    assert 'line 15, in add_try_except' in res
    json_dict = json.loads(res)
    for item in FIELD_LIST:
        assert item in json_dict
    for item in ADDITIONAL_DEBUG_FIELDS:
        assert item not in json_dict


def test_custom_default_formatter_with_stack_info(mocker):
    mocker.patch("fastapi_example.config.Config.JSON_LOG_FORMAT", new=False)

    formatter = custom_formatter.CustomFormatter(
        '%(asctime)s %(compid)s %(levelname)-7s %(correlation_id)-36s %(message)s',
        EXTRA_FIELDS_MAP
    )

    err_msg = 'Internal server error: division by zero'
    log_rec_with_stack_info = LogRecord("test", 40, "test", 999, err_msg, (),
                                        sys.exc_info(), 'add_try_except', STACK_INFO_FOR_TEST)
    res = formatter.format(log_rec_with_stack_info)
    assert err_msg in res
    assert 'fastapi_example/api/middlewares/try_except_middleware.py' in res
    assert 'line 15, in add_try_except' in res
    assert "test:999" not in res
    assert "MainThread" not in res


def test_custom_long_json_formatter_with_stack_info(mocker):
    mocker.patch("fastapi_example.config.Config.JSON_LOG_FORMAT", new=True)
    mocker.patch("fastapi_example.config.Config.LONG_LOG_LINE", new=True)

    formatter = custom_formatter.CustomFormatter(
        '%(asctime)s %(compid)s %(levelname)-7s %(correlation_id)-36s %(message)s',
        EXTRA_FIELDS_MAP
    )

    err_msg = 'Internal server error: division by zero'
    log_rec_with_stack_info = LogRecord("test", 40, "test", 999, err_msg, (),
                                        sys.exc_info(), 'add_try_except', STACK_INFO_FOR_TEST)
    res = formatter.format(log_rec_with_stack_info)
    assert err_msg in res
    assert 'fastapi_example/api/middlewares/try_except_middleware.py' in res
    assert 'line 15, in add_try_except' in res
    json_dict = json.loads(res)
    for item in FIELD_LIST:
        assert item in json_dict

    for item in ADDITIONAL_DEBUG_FIELDS:
        assert item in json_dict


def test_custom_long_default_formatter_with_stack_info(mocker):
    mocker.patch("fastapi_example.config.Config.JSON_LOG_FORMAT", new=False)
    mocker.patch("fastapi_example.config.Config.LONG_LOG_LINE", new=True)

    formatter = custom_formatter.CustomFormatter(
        '%(asctime)s %(compid)s %(levelname)-7s %(correlation_id)-36s %(message)s',
        EXTRA_FIELDS_MAP
    )

    err_msg = 'Internal server error: division by zero'
    log_rec_with_stack_info = LogRecord("test", 40, "test", 999, err_msg, (),
                                        sys.exc_info(), 'add_try_except', STACK_INFO_FOR_TEST)
    res = formatter.format(log_rec_with_stack_info)
    assert err_msg in res
    assert 'fastapi_example/api/middlewares/try_except_middleware.py' in res
    assert 'line 15, in add_try_except' in res

    with pytest.raises(JSONDecodeError) as e:
        json.loads(res)
    msg = 'Extra data: line 1 column 5 (char 4)'
    assert e.value.args[0] == msg
    res_lines = res.split("\n")

    m1 = 'fastapi_example-test111 ERROR                                        Internal server error: division by zero'
    m2 = '  File "/FORTESTS/fastapi_example/api/middlewares/try_except_middleware.py", line 15, in add_try_except'

    assert m1 in res_lines[0]
    assert "test:999 MainThread" in res_lines[0]
    assert m2 in res_lines


def test_custom_formatter():
    formatter = custom_formatter.CustomFormatter(
        '%(asctime)s %(compid)s %(levelname)-7s %(correlation_id)-36s %(message)s',
        EXTRA_FIELDS_MAP,
    )

    log_rec_with_health = LogRecord("test", 20, "test", 999, '___test___ %s - "%s %s HTTP/%s" %d ___test___',
                                    ('127.0.0.1:99999', 'GET', '/health', '1.1', 200), None)

    res = formatter.format(log_rec_with_health)
    assert "health" in res


def test_time_formatter():
    formatter = custom_formatter.CustomFormatter(
        '%(asctime)s %(levelname)s %(threadName)d %(funcName) %(message)s %(pathname)s',
        EXTRA_FIELDS_MAP,
    )

    log_rec_with_health = LogRecord("test", 20, "test", 999, '___test___ %s - "%s %s HTTP/%s" %d ___test___',
                                    ('127.0.0.1:99999', 'GET', '/health', '1.1', 200), None)

    res = formatter.formatTime(log_rec_with_health, "%Y-%m-%dT%H:%M:%S")
    s1 = re.search("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", res)
    assert s1.pos == 0

    res2 = formatter.formatTime(log_rec_with_health, "%Y-%m-%d__T__%H:%M:%S")
    s2 = re.search("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]__T__[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", res2)

    assert s2.pos == 0
