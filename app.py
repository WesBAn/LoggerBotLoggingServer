import quart
from werkzeug import exceptions as response_exc

from bot_logging_server.api import send_logs
from bot_logging_server.config import quart_config
from bot_logging_server.models.http.responses import send_logs_post_responses

app = quart.Quart(__name__)


@app.route("/", methods=["GET", "HEAD"])
async def index():
    raise response_exc.NotFound


@app.route("/send_logs", methods=["POST"])
async def get_logs():
    return await send_logs.handle(quart.request)


# @app.errorhandler(send_logs_post_responses.ErrorResponse)
# def handle_error_response(error_response: send_logs_post_responses.ErrorResponse):
#     return _build_flask_error_response(error_response)
#
#
# def _build_flask_error_response(error_response: send_logs_post_responses.ErrorResponse):
#     flask_error_response = flask.jsonify(error_response.response)
#     flask_error_response.status_code = error_response.code
#     return flask_error_response


if __name__ == "__main__":
    app.run(host=quart_config.HOST, port=quart_config.PORT, debug=True)
