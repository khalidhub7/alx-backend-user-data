#!/usr/bin/env python3
""" regex-ing """
import re
import logging
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """ obfuscate specified fields
in a log message """
    msgsplit = message.split(separator)
    msgdict = {}
    for i in msgsplit:
        if i:
            key, value = i.split('=', 1)
            msgdict[key] = value
    for field in fields:
        if field in msgdict:
            message = re.sub(
                "{}={}".format(field, msgdict[field]),
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
        super(RedactingFormatter, self
              ).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord
               ) -> str:
        """ format the log record """
        record.msg = filter_datum(
            self.fields, RedactingFormatter.REDACTION,
            record.msg, RedactingFormatter.SEPARATOR)
        return super().format(record)
