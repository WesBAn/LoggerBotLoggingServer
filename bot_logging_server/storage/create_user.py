import hashlib

from bot_logging_server.storage.mysql import create_user as mysql_create_user
from bot_logging_server.models.http import requests
from bot_logging_server.models.mysql import users, db_connection


async def create_user(
    request: requests.CreateUserPostRequest, mysql_worker: db_connection.MysqlWorker
) -> None:
    """
    Get user id from db

    :param request:
    :param mysql_worker:
    """
    username = request.body.user
    password = request.body.password
    tel_id = request.body.tel_id

    user_token = hashlib.md5((username + password).encode("UTF-8")).hexdigest()

    user = users.User.build_user_to_add(
        username=username, user_token=user_token, tel_id=tel_id
    )
    await mysql_create_user.create_user(user=user, mysql_worker=mysql_worker)
