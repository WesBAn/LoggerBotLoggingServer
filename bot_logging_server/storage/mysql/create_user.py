import logging

from bot_logging_server.models.mysql import users, db_connection
from bot_logging_server.storage.mysql import utils

logger = logging.getLogger("quart.serving")  # pylint: disable=C0103


async def create_user(
    user: users.User, mysql_worker: db_connection.MysqlWorker
) -> None:
    async with mysql_worker.sql_cursor() as cursor:
        query = utils.get_parsed_query_from_file(
            "create_user.sql", user.username, user.tel_id, user.user_token
        )
        await cursor.execute(query)
