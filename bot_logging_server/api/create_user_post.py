import asyncio
import logging
import typing

import quart

from bot_logging_server.models.http import requests, headers
from bot_logging_server.models.http import utils as http_utils
from bot_logging_server.storage import create_user
from bot_logging_server.models.mysql import db_connection

logger = logging.getLogger("quart.serving")  # pylint: disable=C0103


async def handle(
        quart_request: quart.request,
        mysql_user: str,
        mysql_password: str,
        api_key: str
) -> typing.Tuple[typing.Dict, int, typing.Dict]:
    """
    Base function to handle /create_user POST request
    Checks if user is authorized and write logs to mysql db

    Throws:
        quart.exceptions.Forbidden
        quart.exceptions.BadRequest

    :param mysql_user:
    :param mysql_password:
    :param quart_request:
    :param api_key:
    :return: 200 response
    """
    try:
        request = await requests.CreateUserPostRequest.build(quart_request)
        if request.headers.x_api_key != api_key:
            raise quart.exceptions.Forbidden

        mysql_worker = db_connection.MysqlWorker(
            asyncio.get_event_loop(), user=mysql_user, password=mysql_password
        )
        await create_user.create_user(request=request, mysql_worker=mysql_worker)
        return (
            {"code": 200, "message": "User added"},
            200,
            {"Content-Type": headers.JSON_CONTENT_TYPE},
        )
    except http_utils.RequestParsingFailedError:
        logger.error("Request is incorrect")
        raise quart.exceptions.BadRequest
