from logging import LogRecord

from fastapi_example.logging.utils import FilterUvicornAccessLogForHealthEndpoint


def test_filter():
    console_filter = FilterUvicornAccessLogForHealthEndpoint()
    log_rec_with_health = LogRecord("test", 20, "test", 999, '___test___ %s - "%s %s HTTP/%s" %d ___test___',
                                    ('127.0.0.1:99999', 'GET', '/health', '1.1', 200), None)
    log_rec_without_health = LogRecord("test", 20, "test", 999, '___test___ %s - "%s %s HTTP/%s" %d ___test___',
                                       ('127.0.0.1:99999', 'GET', '/test', '1.1', 200), None)

    assert not console_filter.filter(log_rec_with_health)
    assert console_filter.filter(log_rec_without_health)
