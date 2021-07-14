from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get('/bad_route', response_class=PlainTextResponse)
async def default_endpoint():
    """
    Raise RuntimeError whenever called.
    This is just to demo exceptions in the toy app.
    It should be deleted when writing a real world app.
    """

    raise RuntimeError(f"This error was expected as you called the 'bad_route' endpoint")
