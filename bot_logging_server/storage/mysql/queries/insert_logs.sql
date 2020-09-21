# $0 - inserting values

INSERT INTO users_logs
    (user_id,
     pid,
     p_name,
     p_description,
     log_level,
     log_msg,
     log_event_at,
     post_time)
VALUES $0
