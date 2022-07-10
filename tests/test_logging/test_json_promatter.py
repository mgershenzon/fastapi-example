import re
import sys
from logging import LogRecord

import fastapi_example.logging.json_formatter as json_formatter

FIELD_MAP = {
    'asctime': 'time',
    'levelname': 'levelname',
    'threadName': 'threadname',
    'funcName': 'funcname',
    'message': 'message',
    'pathname': 'pathname'
}
EXTRA_FIELDS = {'compid': 'fastapi_example-test111'}

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


def test_json_fomatter_with_stack_info():

    fmter = json_formatter.JSONFormatter(
        '%(asctime)s %(levelname)s %(threadName)d %(funcName) %(message)s %(pathname)s',
        FIELD_MAP,
        EXTRA_FIELDS
    )

    err_msg = 'Internal server error: division by zero'
    log_rec_with_stack_info = LogRecord("test", 40, "test", 999, err_msg, (),
                                        sys.exc_info(), 'add_try_except', STACK_INFO_FOR_TEST)
    res = fmter.format(log_rec_with_stack_info)
    assert err_msg in res
    assert '/fastapi_example/api/middlewares/try_except_middleware.py\\", line 15, in add_try_except' in res


def test_json_fomatter():

    fmter = json_formatter.JSONFormatter(
        '%(asctime)s %(levelname)s %(threadName)d %(funcName) %(message)s %(pathname)s',
        FIELD_MAP,
        EXTRA_FIELDS
    )

    log_rec_with_health = LogRecord("test", 20, "test", 999, '___test___ %s - "%s %s HTTP/%s" %d ___test___',
                                    ('127.0.0.1:99999', 'GET', '/health', '1.1', 200), None)

    res = fmter.format(log_rec_with_health)
    assert "health" in res


def test_time_fomatter():

    fmter = json_formatter.JSONFormatter(
        '%(asctime)s %(levelname)s %(threadName)d %(funcName) %(message)s %(pathname)s',
        FIELD_MAP,
        EXTRA_FIELDS
    )

    log_rec_with_health = LogRecord("test", 20, "test", 999, '___test___ %s - "%s %s HTTP/%s" %d ___test___',
                                    ('127.0.0.1:99999', 'GET', '/health', '1.1', 200), None)

    res = fmter.formatTime(log_rec_with_health, "%Y-%m-%dT%H:%M:%S")
    s1 = re.search("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", res)
    assert s1.pos == 0

    res2 = fmter.formatTime(log_rec_with_health, "%Y-%m-%d__T__%H:%M:%S")
    s2 = re.search("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]__T__[0-9][0-9]:[0-9][0-9]:[0-9][0-9]", res2)

    assert s2.pos == 0
