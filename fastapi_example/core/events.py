import logging
from typing import Callable

from fastapi import FastAPI

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        try:
            # In some apps DB connections are opened here
            logger.info(
                f'Start app handler (This will be printed once per worker). Code can be found in file {__file__}'
            )
        except Exception as e:
            logger.error(f"Error in start_app: {e}")

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        try:
            # In some apps DB connections are closed here
            logger.info(
                f'Stop app handler (This will be printed once per worker). Code can be found in file {__file__}'
            )
        except Exception as e:
            logger.error(f"Error in stop_app: {e}")

    return stop_app
