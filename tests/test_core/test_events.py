import asyncio
from unittest.mock import MagicMock

from fastapi import FastAPI
from starlette.testclient import TestClient

from fastapi_example.core import events
from fastapi_example.core.events import create_start_app_handler, create_stop_app_handler
from fastapi_example.main import app


def test_create_stop_start_app_handlers():
    info_mock = MagicMock()
    events.logger.info = info_mock

    with TestClient(app) as client:
        client.get("/health")
        assert info_mock.call_count == 1

    assert info_mock.call_count == 2


def test_start_app(mocker):
    # Create a mock FastAPI instance
    application = FastAPI()

    # Patch the logger in the module
    mock_logger = mocker.patch('fastapi_example.core.events.logger')

    # Call the create_start_app_handler function to get the start_app handler
    start_app = create_start_app_handler(application)

    # Call the start_app handler explicitly
    asyncio.run(start_app())

    # Assert that logger.info was called
    mock_logger.info.assert_called_once()


def test_start_app_exception(mocker):
    # Create a mock FastAPI instance
    application = FastAPI()

    # Patch the logger in the module
    mock_logger = mocker.patch('fastapi_example.core.events.logger')

    # Set the mock logger to raises an exception when info is called
    mock_logger.info.side_effect = Exception("Test exception")

    # Call the create_start_app_handler function to get the start_app handler
    start_app = create_start_app_handler(application)

    # Call the start_app handler explicitly
    asyncio.run(start_app())

    # Assert that logger.error was called
    mock_logger.error.assert_called_once_with("Error in start_app: Test exception")


def test_stop_app_exception(mocker):
    # Create a mock FastAPI instance
    application = FastAPI()

    # Patch the logger in the module
    mock_logger = mocker.patch('fastapi_example.core.events.logger')

    # Set the mock logger to raises an exception when info is called
    mock_logger.info.side_effect = Exception("Test exception")

    # Call the create_start_app_handler function to get the stop_app handler
    stop_app = create_stop_app_handler(application)

    # Call the stop_app handler explicitly
    asyncio.run(stop_app())

    # Assert that logger.error was called
    mock_logger.error.assert_called_once_with("Error in stop_app: Test exception")
