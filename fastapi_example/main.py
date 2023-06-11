import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_profiler import PyInstrumentProfilerMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi_example.api.errors.http_error import custom_404_handler, http_error_handler
from fastapi_example.api.group_routers import router
from fastapi_example.api.middlewares.try_except_middleware import add_try_except
from fastapi_example.api.middlewares.useful_headers_middleware import add_useful_headers
from fastapi_example.config import Config
from fastapi_example.core.events import create_start_app_handler, create_stop_app_handler
from fastapi_example.logging.utils import setup_logger


def get_application():
    application = FastAPI(title=Config.TITLE, debug=Config.DISPLAY_TRACEBACK_ON_500, version=Config.VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=Config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Adding order is important for middlewares
    application.add_middleware(BaseHTTPMiddleware, dispatch=add_try_except)
    application.add_middleware(BaseHTTPMiddleware, dispatch=add_useful_headers)
    if Config.PROFILING_ON:
        application.add_middleware(PyInstrumentProfilerMiddleware)

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(404, custom_404_handler)

    application.include_router(router)

    return application


app = get_application()


def main():
    setup_logger(Config.LOGGING_CONFIG)
    logger = logging.getLogger("fastapi_example")

    logger.info(
        f'fastapi-example app is about to start. Host: {Config.HOST}, port: {Config.PORT}, workers: {Config.WORKERS}'
    )
    try:
        uvicorn.run(
            "main:app",
            host=Config.HOST,
            port=Config.PORT,
            log_config=Config.LOGGING_CONFIG,
            workers=Config.WORKERS
        )
    except SystemExit as e:
        logger.error(
            f"Problem with uvicorn run. exit code '{e.code}'. Check that host and port and correct and free."
            f" host: '{Config.HOST}', port: '{Config.PORT}''"
        )
        raise RuntimeError(f"Problem with uvicorn. Exit code: '{e.code}'")

    logger.info(f'fastapi-example stopped. Host: {Config.HOST}, port: {Config.PORT}, threads: {Config.WORKERS}')


if __name__ == '__main__':
    main()  # pragma: no cover
