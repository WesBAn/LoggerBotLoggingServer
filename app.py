import flask
from werkzeug import exceptions as response_exc

from bot_logging_server.config import flask_config
from bot_logging_server.models.http import headers
from bot_logging_server.models.http import responses


JSON_CONTENT_TYPE = "application/json"

app = flask.Flask(__name__)


@app.route("/", methods=["GET", "HEAD"])
def index():
    raise response_exc.NotFound


@app.route("/send_logs", methods=["POST"])
def get_logs():
    if flask.request.headers.get(headers.X_CONTENT_TYPE) != JSON_CONTENT_TYPE:
        raise responses.ErrorResponse(
            code=response_exc.BadRequest.code,
            message=responses.ResponseMessagesEnum.INCORRECT_REQUEST_JSON.value,
        )

    user_token = flask.request.headers.get(headers.X_USER_TOKEN)
    if not user_token:  # TODO or user_token is not in DB
        raise responses.ErrorResponse(
            code=response_exc.Forbidden.code,
            message=responses.ResponseMessagesEnum.WRONG_USER_TOKEN.value,
        )


@app.errorhandler(responses.ErrorResponse)
def handle_error_response(error_response: responses.ErrorResponse):
    return __build_flask_error_response(error_response)


def __build_flask_error_response(error_response: responses.ErrorResponse):
    flask_error_response = flask.jsonify(error_response.response)
    flask_error_response.status_code = error_response.code
    return flask_error_response


if __name__ == "__main__":
    app.run(host=flask_config.HOST, port=flask_config.PORT, debug=True)
