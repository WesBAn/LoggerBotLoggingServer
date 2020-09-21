import dataclasses
import datetime
import enum
import typing


class LogLevel(enum.Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclasses.dataclass
class UserLog:
    """
    Class used in writing logs to db

    Methods:
        build() - build instance
    """

    user_id: int
    pid: int
    p_name: str
    log_level: LogLevel
    log_msg: str
    log_event_at: datetime.datetime
    post_time: datetime.datetime
    p_description: str

    @classmethod
    def build(
        cls,
        user_id: int,
        pid: int,
        p_name: str,
        log_level: typing.Union[str, LogLevel],
        log_msg: str,
        log_event_at: datetime.datetime,
        post_time: datetime.datetime,
        p_description: str,
    ) -> "UserLog":
        return cls(
            user_id=user_id,
            pid=pid,
            p_name=p_name,
            log_level=log_level,
            log_msg=log_msg,
            log_event_at=log_event_at,
            post_time=post_time,
            p_description=p_description,
        )
