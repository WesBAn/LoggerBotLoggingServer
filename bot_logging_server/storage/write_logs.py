from bot_logging_server.storage.mysql import insert_logs
from bot_logging_server.models.http import requests
from bot_logging_server.models.mysql import logs, db_connection


async def write_logs(
    user_id: int,
    request: requests.SendLogsPostRequest,
    mysql_worker: db_connection.MysqlWorker,
) -> None:
    """
    Write logs to db

    :param user_id:
    :param request:
    :param mysql_worker:
    :return:
    """
    data = request.body.data
    user_logs_to_write = [
        logs.UserLog.build(
            user_id=user_id,
            pid=data.pid,
            p_name=data.p_name,
            log_level=log.level,
            log_msg=log.msg,
            log_event_at=log.event_at,
            post_time=data.post_time,
            p_description=log.p_description,
        )
        for log in data.logs
    ]
    await insert_logs.insert_logs(mysql_worker=mysql_worker, logs_=user_logs_to_write)
