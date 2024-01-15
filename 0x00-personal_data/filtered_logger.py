#!/usr/bin/env python3
"""Encrypt user data
"""

import bcrypt as b
import logging
import re
from typing import List


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
