import datetime


def test_utils_parsing_query(query_utils):
    result = query_utils.get_parsed_query_from_file("get_user.sql", "user", "token")
    assert (
        result
        == "SELECT * FROM users WHERE username = 'user' AND user_token = 'token';"
    )


def test_inserting_logs_in_insert_query(query_utils, logs):
    log_level = logs.LogLevel("error")
    time = datetime.datetime.utcnow()
    str_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log1 = logs.UserLog.build(
        1, 123, "p_name_val", log_level, "msg", time, time, "descr"
    )
    log2 = logs.UserLog.build(
        1, 123, "p_name_val2", log_level, "msg2", time, time, "descr2"
    )

    result = query_utils.make_insert_logs_values_query_from_file(
        "insert_logs.sql", [log1, log2]
    )
    assert result == (
        "INSERT INTO users_logs (user_id, pid, p_name, p_description, log_level, "
        "log_msg, log_event_at, post_time) VALUES (1, 123, 'p_name_val', 'descr', "
        f"'error', 'msg', '{str_time}', '{str_time}'), (1, 123, "
        f"'p_name_val2', 'descr2', 'error', 'msg2', '{str_time}', '{str_time}')"
    )
