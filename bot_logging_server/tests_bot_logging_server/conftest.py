# pylint: disable=wildcard-import, unused-wildcard-import, redefined-outer-name
# pylint: disable=C0415
import pytest


@pytest.fixture(name="logging_app")
def _logging_app():
    from app import app

    return app.test_client()


@pytest.fixture(name="query_utils")
def _utils():
    from bot_logging_server.storage.mysql import utils

    return utils


@pytest.fixture(name="logs")
def _logs():
    from bot_logging_server.models.mysql import logs

    return logs
