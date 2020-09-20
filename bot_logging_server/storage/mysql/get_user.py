import typing
import logging

from bot_logging_server.models.mysql import users
from bot_logging_server.models.mysql import db_connection
from bot_logging_server.storage.mysql import utils

logger = logging.Logger(__name__)


async def get_user(
    user: users.User, mysql_worker: db_connection.MysqlWorker
) -> typing.Optional[dict]:
    async with mysql_worker.sql_cursor() as cursor:
        query = utils.get_parsed_query_from_file(
            "get_user.sql", user.username, user.user_token
        )
        await cursor.execute(query)
        result = [row for row in await cursor.fetchall()]
        if len(result) > 1:
            logger.warning("Amount of returned users is more than 1")
            return None
        return result[0] if len(result) == 1 else None
