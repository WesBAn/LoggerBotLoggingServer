import datetime

from bot_logging_server.models.http import headers
from bot_logging_server.models.mysql import logs
from bot_logging_server.config import config


class BadRequestArgs(Exception):
    """Request is invalid"""


def check_headers_passed_correctly(x_user_token: str, x_content_type: str) -> None:
    if x_content_type != headers.JSON_CONTENT_TYPE:
        raise headers.WrongHeadersError("X-Content-Type is incorrect")
    if (
        not isinstance(x_user_token, str)
        or len(x_user_token.split()) != 1
        and len(x_user_token) != config.USER_TOKEN_LENGTH
    ):
        raise headers.WrongHeadersError("X-Content-Type is incorrect")


def check_str_args_are_one_word_and_not_empty(*args) -> None:
    for arg in args:
        if not isinstance(arg, str) or len(arg.strip()) == 0 or len(arg.split()) != 1:
            raise BadRequestArgs("Str argument is provided incorrectly")


def check_str_args_not_empty(*args) -> None:
    for arg in args:
        if not isinstance(arg, str) or len(arg.strip()) == 0:
            raise BadRequestArgs("Str argument is provided incorrectly")


def check_unsigned_args(*args) -> None:
    for arg in args:
        if not isinstance(arg, int) or arg < 0:
            raise BadRequestArgs("Unsigned argument is provided incorrectly")


def try_get_datetime(time: str) -> datetime.datetime:
    if not isinstance(time, str):
        raise BadRequestArgs("Can not parse datetime")
    try:
        parsed_time = datetime.datetime.fromisoformat(time)
        return datetime.datetime.utcfromtimestamp(parsed_time.timestamp())
    except ValueError:
        raise BadRequestArgs("Can not parse datetime")


def try_get_log_level(log_level: str) -> logs.LogLevel:
    if not isinstance(log_level, str):
        raise BadRequestArgs("log_level is incorrect")
    try:
        result = logs.LogLevel(log_level)
        return result
    except ValueError:
        raise BadRequestArgs("log_level is incorrect")
