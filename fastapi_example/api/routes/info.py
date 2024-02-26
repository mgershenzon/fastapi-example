import logging

from fastapi import APIRouter

from fastapi_example.utils.info import service_info

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/info')
async def info():
    """
    Returns information about the service"

    :return: information about the service
    """
    logger.info(f'Info about the service: {service_info}')
    return service_info
