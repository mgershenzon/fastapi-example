from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


def create_response_for_errors(exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return create_response_for_errors(exc)


async def custom_404_handler(req, http_exception):
    msg = f"Url '{req.url}' not found, details: '{http_exception.detail}'"
    return create_response_for_errors(HTTPException(status_code=404, detail=msg))
