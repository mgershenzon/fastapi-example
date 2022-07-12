from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def default_endpoint(request: Request):
    """
    Return 'OK!' response of the service is alive

    :return: 'OK!' string
    """
    return 'Hi! This is the root level. Try <a href="docs"> %sdocs </a> endpoint :)' % request.url
