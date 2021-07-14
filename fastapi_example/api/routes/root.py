from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get('/', response_class=PlainTextResponse)
async def default_endpoint():
    """
    Return 'OK!' response of the service is alive

    :return: 'OK!' string
    """
    return 'Hi! This is the root level. Try calling `/docs` endpoint :)'
