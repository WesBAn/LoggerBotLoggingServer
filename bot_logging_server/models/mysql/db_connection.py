import asyncio
import aiomysql
import contextlib
import logging

from bot_logging_server.config import config

logger = logging.getLogger("quart.serving")


class MysqlWrongAuthParams(Exception):
    """User or password is None"""


class ConnectionFailed(Exception):
    """Connection to db was not established"""


class CursorFailed(Exception):
    """Got fail when was creating the cursor"""


class MysqlWorker:
    """
    Sql class which provided async context manager to work with db

    Methods:
        sql_cursor() - cursor context manager used for performing sql requests

        __init__(loop, user, password) - create class instance user and password
        or getting from environment
    """

    def __init__(
        self, loop: asyncio.AbstractEventLoop, user: str, password: str,
    ):
        if user is None or password is None:
            raise MysqlWrongAuthParams("User or password is None")
        self.connect_info = {
            "host": config.MYSQL_HOST,
            "user": user,
            "password": password,
            "port": config.MYSQL_PORT,
            "db": config.DB_NAME,
            "cursorclass": aiomysql.cursors.DictCursor,
            "loop": loop,
        }

    @contextlib.asynccontextmanager
    async def sql_cursor(self):
        async with self._sql_connection() as connection:
            cursor = await connection.cursor()
            try:
                yield cursor
            except Exception as exc:
                logger.error(exc)
                raise CursorFailed("Got fail when was creating the cursor")
            finally:
                await cursor.close()

    @contextlib.asynccontextmanager
    async def _sql_connection(self):
        connection = await aiomysql.connect(**self.connect_info)
        try:
            yield connection
        except CursorFailed as cursor_exc:
            await connection.rollback()
            raise cursor_exc
        except Exception:
            raise ConnectionFailed("Connection to db failed")
        else:
            await connection.commit()
        finally:
            connection.close()
