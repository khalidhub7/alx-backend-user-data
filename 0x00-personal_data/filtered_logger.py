#!/usr/bin/env python3
""" regex-ing """
import re
from typing import AnyStr, List


def filter_datum(
        fields: List[str], redaction: AnyStr,
        message: AnyStr, separator: AnyStr) -> AnyStr:
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
