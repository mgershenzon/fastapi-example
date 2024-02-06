import time
from logging import BASIC_FORMAT, Formatter, LogRecord

from pythonjsonlogger.jsonlogger import JsonFormatter

from fastapi_example.api.middlewares.useful_headers_middleware import get_correlation_id
from fastapi_example.config import Config


class CustomFormatter(Formatter):
    """
    JSON log formatter. Provides users getting logs in JSON format.

    """
    converter = time.gmtime

    def __init__(self, fmt: str = None, extra_fields: dict = None):
        """
        CustomFormatter constructor.
        For further details refer to logging.Formatter.__init__ documentation.
        :param fmt: log record format.
        """

        if Config.LONG_LOG_LINE:
            fmt = fmt + Config.LOG_FORMAT_OPTIONAL_DATA if fmt else BASIC_FORMAT + Config.LOG_FORMAT_OPTIONAL_DATA

        self.internal_formatter = JsonFormatter(fmt=fmt) if Config.JSON_LOG_FORMAT else Formatter(fmt=fmt)
        super(CustomFormatter, self).__init__()

        self._extra_fields = extra_fields or {}

    def format(self, record: LogRecord) -> str:
        """
        Log message formatting.

        :param record: received LogRecord instance
        :return: encoded log message in JSON format
        """
        record.compid = self._extra_fields['compid']
        record.correlation_id = get_correlation_id()

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        log_line = self.internal_formatter.format(record)

        return log_line
