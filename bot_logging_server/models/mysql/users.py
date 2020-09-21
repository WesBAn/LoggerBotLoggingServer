import dataclasses
import typing


@dataclasses.dataclass
class User:
    """
    Class used for getting or creating users

    Methods:
        build_user_to_auth(username, user_token) - builds user instance to check user in db
        build_user_to_add(username, user_token, tel_id) - builds user instance to write user in db
    """

    username: str
    user_token: str
    tel_id: typing.Optional[str]

    @classmethod
    def build_user_to_auth(cls, username: str, user_token: str) -> "User":
        return cls(username=username, user_token=user_token, tel_id=None)

    @classmethod
    def build_user_to_add(cls, username: str, user_token: str, tel_id: str) -> "User":
        return cls(username=username, user_token=user_token, tel_id=tel_id)
