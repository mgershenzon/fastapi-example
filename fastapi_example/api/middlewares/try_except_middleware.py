import logging

from fastapi import HTTPException, Request

from fastapi_example.api.errors.http_error import create_response_for_errors

logger = logging.getLogger(__name__)


async def add_try_except(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        msg = f'Internal server error: {e}'
        logger.exception(msg)
        ex = HTTPException(status_code=500, detail=f'Internal server error: {e}')
        return create_response_for_errors(ex)

    return response
