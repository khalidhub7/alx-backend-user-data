#!/usr/bin/env python3
""" regex-ing """
import re
import logging
from typing import List
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """ obfuscate specified fields
in a log message """
    messageSplit = message.split(separator)[:-1]
    messageDict = {}
    for keyvalue in messageSplit:
        if '=' in keyvalue:
            key, value = keyvalue.split('=', 1)
            messageDict[key] = value
    for field in fields:
        if field in messageDict:

            message = re.sub(
                r"{}=[^;]+".format(field),
                "{}={}".format(field, redaction),
                message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s\
 %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialize """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields
    def format(self, record: logging.LogRecord
               ) -> str:
        """ format the log record """
        record.msg = filter_datum(
            self.fields, RedactingFormatter.REDACTION,
            record.msg, RedactingFormatter.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    create logger named 'user_data'
    logger is like a note"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(PII_FIELDS)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    return logger
