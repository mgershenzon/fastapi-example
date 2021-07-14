import logging
from typing import Callable

from fastapi import FastAPI
from loguru import logger as loguru_logger

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        # In some apps DB connections are opened here
        logger.info(f'Start app handler (This will be printed once per worker). Code can be found in file {__file__}')

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @loguru_logger.catch
    async def stop_app() -> None:
        # In some apps DB connections are closed here
        logger.info(f'Stop app handler (This will be printed once per worker). Code can be found in file {__file__}')

    return stop_app
