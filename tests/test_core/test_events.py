from fastapi_example.core.events import create_start_app_handler, create_stop_app_handler
from fastapi_example.main import app


def test_create_start_app_handler():
    create_start_app_handler(app)


def test_create_stop_app_handler():
    create_stop_app_handler(app)
