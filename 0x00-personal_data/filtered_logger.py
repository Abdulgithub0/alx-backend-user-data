#!/usr/bin/env python3
"""Encrypt user data
"""

import bcrypt as b
import logging
import re
from typing import List


def filter_datum(fields: List,
                 redaction: str,
                 message: str,
                 separator: str
                 ) -> str:
    """
    :params:
        fields: a list of strings representing all fields
            to obfuscate
        redaction: a string representing by what
            the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character
            is separating all fields in the log line (message)
    :return: strings of encrypt data based on redaction supply
    """
    for data in fields:
        message = re.sub(r"{}=[^{}]*".format(data, separator),
                         "{}={}".format(data, redaction), message)
    return message
