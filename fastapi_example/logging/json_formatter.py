import json
import re
import time
from logging import Formatter, LogRecord
from typing import List

from fastapi_example.api.middlewares.useful_headers_middleware import get_correlation_id


class JSONFormatter(Formatter):
    """
    JSON log formatter. Provides users getting logs in JSON format.

    """
    converter = time.gmtime

    def __init__(self, fmt: str = None, fields_mapping: dict = None, extra_fields: dict = None):
        """
        JSONFormatter constructor.
        For further details refer to logging.Formatter.__init__ documentation.
        :param fmt: log record format.
        :param datefmt: log record date format
        """
        super(JSONFormatter, self).__init__()

        self._fmt = fmt
        self.fields_mapping = fields_mapping or {}
        self._extra_fields = extra_fields or {}

    def parse(self) -> List[str]:
        """
        Parse the format to extract needed parameters.

        :return: list of parameters
        """
        standard_formatters = re.compile(r'\((.+?)\)', re.IGNORECASE)
        return standard_formatters.findall(self._fmt)

    def format(self, record: LogRecord) -> str:
        """
        Log message formatting.

        :param record: received LogRecord instance
        :return: encoded log message in JSON format
        """
        record.message = record.getMessage()
        record.asctime = self.formatTime(record)

        params = self.parse()

        json_log_record = {
            'time': self.fields_mapping['asctime'],
            'compid': self._extra_fields['compid'],
            'correlationid': get_correlation_id(),
        }

        json_log_record.update({param: getattr(record, param) for param in params})

        for k, v in self.fields_mapping.items():
            json_log_record[v] = json_log_record.pop(k)

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            json_log_record['stack_trace'] = record.exc_text
        if record.stack_info:
            json_log_record['stack_info'] = self.formatStack(record.stack_info)

        return json.dumps(json_log_record)

    def formatTime(self, record: LogRecord, datefmt: str = None):
        """
        Time stamp formatting method.

        :param record: received LogRecord instance
        :param datefmt: date format pattern string
        :return:
        """
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%dT%H:%M:%S", ct)
            s = "%s.%03dZ" % (t, record.msecs)
        return s
