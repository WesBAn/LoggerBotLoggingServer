import typing

from bot_logging_server.storage.mysql import get_user
from bot_logging_server.models.http import requests
from bot_logging_server.models.mysql import users, db_connection


async def get_user_id(
    request: requests.SendLogsPostRequest, mysql_worker: db_connection.MysqlWorker
) -> typing.Optional[int]:
    username = request.body.data.user
    user_token = request.headers.x_user_token

    user = users.User.build_user_to_auth(username=username, user_token=user_token)
    user_matched = await get_user.get_user(user=user, mysql_worker=mysql_worker)
    return user_matched["id"] if user_matched is not None else None
