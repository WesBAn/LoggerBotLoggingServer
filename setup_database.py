import logging
import click
import pymysql

from bot_logging_server.config import config

HOST = "localhost"

CREATE_DB_QUERY = f"CREATE DATABASE {config.DB_NAME};"
CREATE_USER_TABLE = """
    CREATE TABLE `users` (
    `id` int(10) unsigned NOT NULL auto_increment,
    `username` VARCHAR(100) NOT NULL,
    `tel_id` VARCHAR(100) NOT NULL,
    `user_token` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`username`))
    CHARSET=utf8mb4;
"""
CREATE_LOGS_TABLE = """
    CREATE TABLE `users_logs` (
    `id` int(10) unsigned NOT NULL auto_increment,
    `user_id` int(10) unsigned NOT NULL,
    `pid` int(10) NOT NULL,
    `p_name` VARCHAR(100) NOT NULL,
    `p_description` VARCHAR(100) NOT NULL,
    `log_level` ENUM('error', 'warning') NOT NULL,
    `log_msg` VARCHAR(100) NOT NULL,
    `log_event_at` DATETIME NOT NULL,
    `post_time` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES users (`id`) ON DELETE CASCADE)
    ENGINE = InnoDB, CHARSET = utf8mb4;
"""

logger = logging.getLogger(__name__)


def _setup_db(user, password, port, host=HOST):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_DB_QUERY)
        cursor.execute(f"USE {config.DB_NAME};")
        cursor.execute(CREATE_USER_TABLE)
        cursor.execute(CREATE_LOGS_TABLE)
    except Exception as exc:
        connection.rollback()
        raise Exception from exc
    finally:
        cursor.close()
        connection.commit()

    connection.close()


@click.command()
@click.option("--user", type=str, required=True, help="Username")
@click.option("--password", type=str, required=True, help="Password")
@click.option("--port", type=int, required=True, default=8889, help="Port")
def main(user, password, port):
    _setup_db(user=user, password=password, port=port)


def testing_main(user, password, port, host):
    _setup_db(user=user, password=password, port=port, host=host)


if __name__ == "__main__":
    main()
