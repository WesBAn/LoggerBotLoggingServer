import dataclasses
import typing


@dataclasses.dataclass
class User:
    username: str
    user_token: str
    tel_id: typing.Optional[str]

    @classmethod
    def build_user_to_auth(cls, username: str, user_token: str) -> "User":
        return cls(username=username, user_token=user_token, tel_id=None)

    @classmethod
    def build_user_to_add(cls, username: str, user_token: str, tel_id: str) -> "User":
        return cls(username=username, user_token=user_token, tel_id=tel_id)

    # TODO Maybe unused
    def serialize(self) -> typing.Dict[str, typing.Optional[str]]:
        return {
            "username": self.username,
            "user_token": self.user_token,
            "tel_id": self.tel_id,
        }
