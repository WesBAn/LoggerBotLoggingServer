import quart
from bot_logging_server.api import send_logs
from bot_logging_server.config import quart_config
from bot_logging_server.models.http import headers

app = quart.Quart(__name__)


@app.route("/", methods=["GET", "HEAD"])
async def index():
    quart.abort(404)


@app.route("/send_logs", methods=["POST"])
async def send_logs_():
    try:
        return await send_logs.handle(quart.request)
    except quart.exceptions.BadRequest:
        return {"code": 400, "message": "BadRequest"}, 400, {'Content-Type': headers.JSON_CONTENT_TYPE}
    except quart.exceptions.Forbidden:
        return {"code": 403, "message": "Forbidden"}, 403, {'Content-Type': headers.JSON_CONTENT_TYPE}


if __name__ == "__main__":
    app.run(host=quart_config.HOST, port=quart_config.PORT, debug=True)
