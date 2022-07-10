from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get('/bad_route', response_class=PlainTextResponse)
async def bad_route():
    """
    Raise RuntimeError whenever called.
    This is just to demo exceptions in the toy app.
    It should be deleted when writing a real world app.
    """

    raise RuntimeError(f"This error was expected as you called the 'bad_route' endpoint")


@router.get('/http_404', response_class=PlainTextResponse)
async def http_404():
    """
    Raise HTTPException whenever called.
    This is just to demo exceptions in the toy app.
    It should be deleted when writing a real world app.
    """

    raise HTTPException(status_code=404, detail="This is en example on how 404 error will look like")


@router.get('/some_error_but_return_ok', response_class=PlainTextResponse)
async def some_error_but_return_ok():
    """
    Expected "Internal server error: division by zero" during the call
    but still return OK
    This is just to demo exceptions in the toy app.
    It should be deleted when writing a real world app.
    """
    try:
        1 / 0

    finally:
        return "OK"
