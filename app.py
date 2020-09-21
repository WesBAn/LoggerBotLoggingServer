import os
import click
import quart

from bot_logging_server.api import send_logs
from bot_logging_server.config import quart_config
from bot_logging_server.models.http import headers


ENV_DB_USER = "LOGGER_DB_USER"
ENV_DB_PASSWORD = "LOGGER_DB_PASSWORD"

app = quart.Quart(__name__)

mysql_user = None
mysql_password = None


@app.route("/", methods=["GET", "HEAD"])
async def index():
    """
    No data for / endpoint

    :return: 404
    """
    quart.abort(404)


@app.route("/send_logs", methods=["POST"])
async def send_logs_():
    """
    Receive logs from client to write in db

    If global vars: (mysql_user, mysql_password) are not set
    then get them from environment LOGGER_DB_USER and LOGGER_DB_PASSWORD respectively

    Example of correct request:
    {
        'data': {
           'user': user
           'pid': pid,
        'p_name': process.name(),
        'post_time': "2020-05-05 20:00:00+00:00",
        'logs': [
            {
                'level': level,
                'msg': msg,
                'event_at':msg_datetime,
                'p_description': process_user_desc
            }
        ]
    }

    :return:
        [Logs added] (200) response_description, 200, application/json
        [Forbidden] (403) response_description, 403, application/json
        [BadRequest] (400) response_description, 400, application/json
    """
    try:
        return await send_logs.handle(
            quart_request=quart.request,
            mysql_user=mysql_user if mysql_user is not None else os.getenv(ENV_DB_USER),
            mysql_password=mysql_password
            if mysql_password is not None
            else os.getenv(ENV_DB_PASSWORD),
        )
    except quart.exceptions.BadRequest:
        return (
            {"code": 400, "message": "BadRequest"},
            400,
            {"Content-Type": headers.JSON_CONTENT_TYPE},
        )
    except quart.exceptions.Forbidden:
        return (
            {"code": 403, "message": "Forbidden"},
            403,
            {"Content-Type": headers.JSON_CONTENT_TYPE},
        )
    except Exception:
        return (
            {"code": 500, "message": "Internal Server Error"},
            500,
            {"Content-Type": headers.JSON_CONTENT_TYPE},
        )


@click.command()
@click.option("--host", type=str, help="Host")
@click.option("--port", type=int, help="Port")
@click.option("--user", type=str, help="Mysql Username")
@click.option("--password", type=str, help="Mysql Password")
def main(host, port, user, password):
    """
    Production app run

    :param host: host ip getting from cli argument or quart_config.py
    :param port: port getting from cli argument or quart_config.py
    :param user: mysql user, got from cli. If set then set global mysql_user var
    :param password: mysql password, got from cli. If set then set global mysql_password var
    :return:
    """
    if user is not None:
        global mysql_user
        mysql_user = user
    if password is not None:
        global mysql_password
        mysql_password = password

    app.run(
        host=quart_config.HOST if host is None else host,
        port=quart_config.PORT if port is None else port,
    )


if __name__ == "__main__":
    main()
