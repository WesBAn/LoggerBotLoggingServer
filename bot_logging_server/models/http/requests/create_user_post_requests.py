# pylint: disable=R0801
import dataclasses
import logging
import typing
import quart

from bot_logging_server.models.http import (
    utils as http_utils,
    headers as headers_template,
)

logger = logging.getLogger("quart.serving")  # pylint: disable=C0103


@dataclasses.dataclass(frozen=True)
class CreateUserPostRequest:
    """
    Serializing /create_user request

    Methods:
        build - build class instance
    """

    body: "RequestBody"
    headers: "Headers"

    @classmethod
    async def build(cls, quart_request: quart.Request) -> "CreateUserPostRequest":
        body = await quart_request.get_json(force=True)
        logger.info("Request body: %s", body)
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
    user: str
    password: str
    tel_id: str

    @classmethod
    def build(cls, body_dict: typing.Mapping[str, typing.Any]) -> "RequestBody":
        http_utils.check_str_args_are_one_word_and_not_empty(
            body_dict["user"], body_dict["password"], body_dict["tel_id"]
        )
        return cls(
            user=body_dict["user"],
            password=body_dict["password"],
            tel_id=body_dict["tel_id"],
        )


@dataclasses.dataclass(frozen=True)
class Headers:
    x_api_key: str
    x_content_type: str

    @classmethod
    def build(cls, headers_dict: typing.Mapping[str, str]) -> "Headers":
        x_api_key = headers_dict.get(headers_template.X_API_KEY)
        x_content_type = headers_dict.get(headers_template.X_CONTENT_TYPE)
        http_utils.check_api_key_and_content_type_correct(
            x_content_type=x_content_type, x_api_key=x_api_key
        )
        return cls(x_content_type=x_content_type, x_api_key=x_api_key)
