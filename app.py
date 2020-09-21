import quart

from bot_logging_server.api import send_logs
from bot_logging_server.config import quart_config
from bot_logging_server.models.http import headers

app = quart.Quart(__name__)


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
        return await send_logs.handle(quart.request)
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


if __name__ == "__main__":
    app.run(host=quart_config.HOST, port=quart_config.PORT, debug=True)
