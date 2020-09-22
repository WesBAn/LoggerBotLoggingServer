# pylint: disable=R0801
import dataclasses
import datetime
import logging
import typing

import quart

from bot_logging_server.models.http import (
    utils as http_utils,
    headers as headers_template,
)
from bot_logging_server.models.mysql import logs

logger = logging.getLogger("quart.serving")  # pylint: disable=C0103


@dataclasses.dataclass(frozen=True)
class SendLogsPostRequest:
    """
    Serializing /send_logs request

    Methods:
        build - build class instance
    """

    body: "RequestBody"
    headers: "Headers"

    @classmethod
    async def build(cls, quart_request: quart.Request) -> "SendLogsPostRequest":
        body = await quart_request.get_json(force=True)
        logger.info("Request: %s", body)
        headers = quart_request.headers
        try:
            return cls(body=RequestBody.build(body), headers=Headers.build(headers))
        except (
            KeyError,
            TypeError,
            ValueError,
            headers_template.WrongHeadersError,
            http_utils.BadRequestArgs,
        ) as err:
            logger.error('During parsing request happened %s', err)
            raise http_utils.RequestParsingFailedError from err


@dataclasses.dataclass(frozen=True)
class RequestBody:
    data: "Data"

    @classmethod
    def build(cls, body_dict: typing.Mapping[str, typing.Any]) -> "RequestBody":
        return cls(data=Data.build(body_dict["data"]))


@dataclasses.dataclass(frozen=True)
class Headers:
    x_content_type: str
    x_user_token: str

    @classmethod
    def build(cls, headers_dict: typing.Mapping[str, str]) -> "Headers":
        x_content_type = headers_dict.get(headers_template.X_CONTENT_TYPE)
        x_user_token = headers_dict.get(headers_template.X_USER_TOKEN)
        http_utils.check_user_token_and_content_type_correct(
            x_content_type=x_content_type, x_user_token=x_user_token
        )
        return cls(x_content_type=x_content_type, x_user_token=x_user_token)


@dataclasses.dataclass(frozen=True)
class Data:
    user: str
    pid: int
    p_name: str
    post_time: datetime.datetime
    logs: typing.List["Log"]

    @classmethod
    def build(cls, data_dict: typing.Mapping[str, typing.Any]):
        post_time = http_utils.try_get_datetime(data_dict["post_time"])
        http_utils.check_str_args_are_one_word_and_not_empty(data_dict["user"])
        http_utils.check_str_args_not_empty(data_dict["p_name"])
        http_utils.check_unsigned_args(data_dict["pid"])
        return cls(
            user=data_dict["user"],
            pid=data_dict["pid"],
            p_name=data_dict["p_name"],
            post_time=post_time,
            logs=[Log.build(log) for log in data_dict["logs"]],
        )


@dataclasses.dataclass(frozen=True)
class Log:
    level: logs.LogLevel
    msg: str
    event_at: datetime.datetime
    p_description: str

    @classmethod
    def build(cls, log_dict: typing.Mapping[str, typing.Any]):
        event_at = http_utils.try_get_datetime(log_dict["event_at"])
        level = http_utils.try_get_log_level(log_dict["level"])
        http_utils.check_str_args_not_empty(log_dict["msg"])
        http_utils.check_str_args_not_empty(log_dict["p_description"])
        return cls(
            level=level,
            msg=log_dict["msg"],
            event_at=event_at,
            p_description=log_dict["p_description"],
        )
