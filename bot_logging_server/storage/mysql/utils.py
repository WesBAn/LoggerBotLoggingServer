import os
import datetime
import typing

from bot_logging_server.models.mysql import logs

DEFAULT_PATH = "bot_logging_server/storage/mysql/queries"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_parsed_query_from_file(name: str, *args_to_fill_query) -> str:
    """
    Parse sql query file and replace templates ($0, $1..) by values

    :param name:
    :param args_to_fill_query:
    :return:
    """
    with open(f"{os.getcwd()}/{DEFAULT_PATH}/{name}", "r") as file:
        result_str = " ".join(
            [line.strip() for line in file if line.strip() and not line.startswith("#")]
        )
        for i, arg in enumerate(args_to_fill_query):
            insert_in = "$" + str(i)
            if isinstance(arg, (str, datetime.datetime)):
                arg = "".join(["'", str(arg), "'"])
            result_str = result_str.replace(insert_in, str(arg))
        return result_str


def make_insert_logs_values_query_from_file(
    name: str, values: typing.Iterable[logs.UserLog]
):
    """
    Parse sql query file and replace $0 in 'VALUES $0' by inserting values

    :param name:
    :param values:
    :return:
    """
    logs_in_list = [
        (
            value.user_id,
            value.pid,
            value.p_name,
            value.p_description,
            value.log_level.value,
            value.log_msg,
            value.log_event_at,
            value.post_time,
        )
        for value in values
    ]
    with open(f"{os.getcwd()}/{DEFAULT_PATH}/{name}", "r") as file:
        result_str = " ".join(
            [line.strip() for line in file if line.strip() and not line.startswith("#")]
        )
        values_formatted = _make_values(logs_in_list)
        return result_str.replace("$0", values_formatted)


def _make_values(values):
    result_values = []
    for value in values:
        value_formatted_list = []
        for elem in value:
            if isinstance(elem, datetime.datetime):
                elem = elem.strftime(DATETIME_FORMAT)
            value_formatted_list.append(elem)
        result_values.append(str(tuple(value_formatted_list)))
    return ", ".join(result_values)
