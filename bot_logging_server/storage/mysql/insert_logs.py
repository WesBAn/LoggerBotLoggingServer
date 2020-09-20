import typing

from bot_logging_server.models.mysql import logs
from bot_logging_server.models.mysql import db_connection
from bot_logging_server.storage.mysql import utils


async def insert_logs(
    mysql_worker: db_connection.MysqlWorker, logs_: typing.Iterable[logs.UserLog]
) -> None:
    async with mysql_worker.sql_cursor() as cursor:
        query = utils.make_insert_many_values_query_from_file("insert_logs.sql", logs_)
        await cursor.execute(query)
