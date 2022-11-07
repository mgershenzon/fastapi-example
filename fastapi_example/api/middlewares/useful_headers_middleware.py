import logging
from contextvars import ContextVar
from datetime import datetime
from uuid import uuid4

from fastapi import Request

logger = logging.getLogger(__name__)


CORRELATION_ID_CTX_KEY = 'correlation_id'

_correlation_id_ctx_var: ContextVar[str] = ContextVar(CORRELATION_ID_CTX_KEY, default="")


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()


async def add_useful_headers(request: Request, call_next):
    start_time = datetime.now()
    correlation_id = _correlation_id_ctx_var.set(request.headers.get('X-Correlation-ID', str(uuid4())))

    response = await call_next(request)

    process_time = (datetime.now() - start_time).microseconds / 1000

    response.headers["X-Process-Time"] = str(process_time)
    response.headers['X-Correlation-ID'] = get_correlation_id()

    if 'health' not in request.url.path:
        logger.info(f"Successfully processed request, processing took {process_time} ms")

    _correlation_id_ctx_var.reset(correlation_id)

    return response
