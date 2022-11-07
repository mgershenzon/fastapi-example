import logging
import logging.config

import yaml

logger = logging.getLogger(__name__)


class FilterUvicornAccessLogForHealthEndpoint(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/health" not in record.args


def setup_logger(conf_file: str):
    """
    Method to initialise logger configuration
    :param conf_file: configuration file
    :return:
    """
    with open(conf_file) as file:
        config: dict = yaml.safe_load(file.read())
        logging.config.dictConfig(config)

        logger.debug(f"Logging was setup with {conf_file} file.")
