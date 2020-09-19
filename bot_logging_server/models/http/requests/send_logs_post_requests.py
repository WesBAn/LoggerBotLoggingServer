import dataclasses
import datetime
import typing

import quart

from bot_logging_server.models.http import headers as headers_template


@dataclasses.dataclass(frozen=True)
class SendLogsPostRequest:
    body: "RequestBody"
    headers: "Headers"

    @classmethod
    def build(cls, quart_request: quart.Request) -> "SendLogsPostRequest":
        body = quart_request.args
        headers = quart_request.headers
        return cls(body=RequestBody.build(body), headers=Headers.build(headers))


@dataclasses.dataclass(frozen=True)
class RequestBody:
    data: "Data"

    @classmethod
    def build(cls, body_dict: typing.Mapping[str, typing.Any]) -> "RequestBody":
        return cls(data=Data.build(body_dict["data"]))


@dataclasses.dataclass(frozen=True)
class Headers:
    content_type: str
    x_user_token: str

    @classmethod
    def build(cls, headers_dict: typing.Mapping[str, str]):
        content_type = headers_dict.get(headers_template.X_CONTENT_TYPE)
        if content_type != headers_template.JSON_CONTENT_TYPE:
            raise headers_template.WrongHeadersError("X-Content-Type is incorrect")

        x_user_token = headers_dict.get(headers_template.X_USER_TOKEN)
        if not x_user_token:  # TODO or user_token is not in DB
            raise headers_template.WrongHeadersError("X-User-Token is empty")

        return cls(content_type=content_type, x_user_token=x_user_token)


@dataclasses.dataclass(frozen=True)
class Data:
    pid: str
    p_description: str
    p_name: str
    post_time: datetime.datetime
    logs: typing.List["Log"]

    @classmethod
    def build(cls, data_dict: typing.Mapping[str, typing.Any]):
        return cls(
            pid=data_dict["pid"],
            p_description=data_dict["p_description"],
            p_name=data_dict["p_name"],
            post_time=datetime.datetime.fromisoformat(data_dict["post_time"]),
            logs=[Log.build(log) for log in data_dict["logs"]],
        )


@dataclasses.dataclass(frozen=True)
class Log:
    level: str
    msg: str
    event_at: str

    @classmethod
    def build(cls, log_dict: typing.Mapping[str, typing.Any]):
        return cls(
            level=log_dict["level"], msg=log_dict["msg"], event_at=log_dict["event_at"],
        )
