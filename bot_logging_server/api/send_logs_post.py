import asyncio
import logging
import typing

import quart

from bot_logging_server.models.http import requests, headers
from bot_logging_server.models.http import utils as http_utils
from bot_logging_server.storage import write_logs, auth_user
from bot_logging_server.models.mysql import db_connection

logger = logging.getLogger("quart.serving")  # pylint: disable=C0103


async def handle(
        quart_request: quart.request,
        mysql_user: str,
        mysql_password: str,
) -> typing.Tuple[typing.Dict, int, typing.Dict]:
    """
    Base function to handle /send_logs POST request
    Checks if user is authorized and write logs to mysql db

    Throws:
        quart.exceptions.Forbidden
        quart.exceptions.BadRequest

    :param mysql_user:
    :param mysql_password:
    :param quart_request:
    :return: 200 response
    """
    try:
        request = await requests.SendLogsPostRequest.build(quart_request)
        mysql_worker = db_connection.MysqlWorker(
            asyncio.get_event_loop(), user=mysql_user, password=mysql_password
        )
        user_id = await auth_user.get_user_id(
            request=request, mysql_worker=mysql_worker
        )
        if user_id is None:
            raise quart.exceptions.Forbidden
        await write_logs.write_logs(
            user_id=user_id, request=request, mysql_worker=mysql_worker
        )
        return (
            {"code": 200, "message": "Logs added successfully"},
            200,
            {"Content-Type": headers.JSON_CONTENT_TYPE},
        )
    except http_utils.RequestParsingFailedError:
        logger.error("Request is incorrect")
        raise quart.exceptions.BadRequest
