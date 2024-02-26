import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/bad_route', response_class=PlainTextResponse)
async def bad_route():
    """
    Raise RuntimeError whenever called.
    This is just to demo exceptions in the toy app.
    It should be deleted when writing a real world app.
    """

    raise RuntimeError("This error was expected as you called the 'bad_route' endpoint")


@router.get('/http_404', response_class=PlainTextResponse)
async def http_404():
    """
    Raise HTTPException whenever called.
    This is just to demo exceptions in the toy app.
    It should be deleted when writing a real world app.
    """

    raise HTTPException(status_code=404, detail="This is an example of how a 404 error will look like")


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
    except Exception as e:
        logger.warning("Warning from the except block after a problem dividing 1 with 0.", exc_info=e)
    finally:
        return "OK"


@router.get('/bad_request_error_for_odd_numbers/{number}')
async def bad_request_error_for_odd_numbers(number: int):
    if number % 2 == 1:
        raise HTTPException(status_code=418, detail="Odd numbers get this error")
    return number
