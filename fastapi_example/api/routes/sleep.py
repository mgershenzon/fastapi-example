import asyncio
import logging
import threading

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/sleep', response_class=PlainTextResponse)
async def sleep(sleep_seconds: int = 0):
    """
    Return sleep_seconds after sleeping for that amount of time and printing to the log

    :return: sleep_seconds int
    """

    for i in range(sleep_seconds):

        # use the non blocking asyncio sleep to get a better feeling of how this works
        await asyncio.sleep(1)

        logger.info(
            'Sleeping in thread `%s` id `%s`. %s from %s seconds completed' %
            (threading.current_thread().name, threading.current_thread().ident, i + 1, sleep_seconds)
        )

    return str(sleep_seconds)
