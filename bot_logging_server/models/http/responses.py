import enum
import typing


class ResponseMessagesEnum(enum.Enum):
    INCORRECT_REQUEST_JSON = 'Post request was provided in wrong format'
    WRONG_USER_TOKEN = 'Wrong user token'


class ErrorResponse(Exception):
    def __init__(self, code: int, message: str):
        Exception.__init__(self)
        self.code = code
        self.response = _build_error_response(code=code, message=message)


def _build_error_response(code: int, message: str) -> typing.Dict[str, str]:
    return {
        'code': str(code),
        'message': message
    }
