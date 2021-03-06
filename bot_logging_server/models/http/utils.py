import datetime

from bot_logging_server.models.http import headers
from bot_logging_server.models.mysql import logs
from bot_logging_server.config import config


LEVEL_TO_LOG_LEVEL_ENUM = {
    30: logs.LogLevel.WARNING,
    40: logs.LogLevel.ERROR,
    50: logs.LogLevel.ERROR,
}


class RequestParsingFailedError(Exception):
    """Request is incorrect"""


class BadRequestArgs(Exception):
    """Request is invalid"""


def check_user_token_and_content_type_correct(
    x_user_token: str, x_content_type: str
) -> None:
    if x_content_type != headers.JSON_CONTENT_TYPE:
        raise headers.WrongHeadersError("X-Content-Type is incorrect")
    if (
        not isinstance(x_user_token, str)
        or len(x_user_token.split()) != 1
        or len(x_user_token) != config.USER_TOKEN_LENGTH
    ):
        raise headers.WrongHeadersError("X-User-Token is incorrect")


def check_api_key_and_content_type_correct(x_api_key: str, x_content_type: str) -> None:
    if x_content_type != headers.JSON_CONTENT_TYPE:
        raise headers.WrongHeadersError("X-Content-Type is incorrect")
    if not isinstance(x_api_key, str) or len(x_api_key.split()) != 1:
        raise headers.WrongHeadersError("X-Api-Key is incorrect")


def check_str_args_are_one_word_and_not_empty(*args) -> None:
    for arg in args:
        if not isinstance(arg, str) or not arg.strip() or len(arg.split()) != 1:
            raise BadRequestArgs("Str argument is provided incorrectly")


def check_str_args_not_empty(*args) -> None:
    for arg in args:
        if not isinstance(arg, str) or not arg.strip():
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
    except ValueError as val_err:
        raise BadRequestArgs("Can not parse datetime") from val_err


def try_get_log_level(log_level: int) -> logs.LogLevel:
    if not isinstance(log_level, int):
        raise BadRequestArgs("log_level is incorrect")
    try:
        result = LEVEL_TO_LOG_LEVEL_ENUM[log_level]
        return result
    except KeyError as key_err:
        raise BadRequestArgs("log_level is incorrect") from key_err
