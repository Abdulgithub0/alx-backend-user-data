#!/usr/bin/env python3
"""Encrypt user data
"""

import bcrypt as b
import logging
import re
from typing import List
from mysql.connector import connection
from os import environ as e
PII_FIELDS = ("name", "email", "phone", "password", "ssn")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    fields: a list of strings representing all fields
        to obfuscate
    redaction: a string representing by what
        the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character
    is separating all fields in the log line (message)
    """
    for data in fields:
        message = re.sub(r"{}=[^{}]*".format(data, separator),
                         "{}={}".format(data, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """obsfucate the value of attr message on record
        """
        record = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            record, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """log user data but obfuscate their PII or personal data
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    redacted_format = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(redacted_format)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """config mysql db and return the connection object
    """
    cn = connection.MySQLConnection(user=e.get("PERSONAL_DATA_DB_USERNAME",
                                               "root"),
                                    password=e.get("PERSONAL_DATA_DB_PASSWORD",
                                                   ""),
                                    host=e.get("PERSONAL_DATA_DB_HOST",
                                               "localhost"),
                                    database=e.get("PERSONAL_DATA_DB_NAME"))
    return cn


if __name__ == "__main__":
    """Obtain a database connection using get_db and retrieve all rows
       in the users table and display each row under a filtered format
    """
    db_conn = get_db()
    if db_conn and db_conn.is_connected():
        logger = get_logger()
        with db_conn.cursor() as cursor:
            cursor.execute("select * from users;")
            rows = cursor.fetchall()
            for row in rows:
                row = "name={}; email={}; phone={}; ssn={}; password={}; "\
                      "ip={}; last_login={}; user_agent={};".format(*row)
                logger.info(row)
        db_conn.close()
