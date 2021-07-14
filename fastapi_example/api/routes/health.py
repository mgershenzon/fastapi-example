from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get('/health', response_class=PlainTextResponse)
async def health():
    """
    Return 'OK!' response of the service is alive

    :return: 'OK!' string
    """
    return 'OK!'


@router.get('/is_ready', response_class=PlainTextResponse)
async def is_ready():
    """
    Return 'OK!' response of the service is ready

    :return: 'OK!' string
    """
    return 'OK!'
