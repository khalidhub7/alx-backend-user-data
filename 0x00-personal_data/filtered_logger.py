#!/usr/bin/env python3
""" regex-ing """
import re
import logging
from os import getenv
from typing import List
from mysql.connector import connect, MySQLConnection
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ hide specific fields in a log message """
    keyvalue = message.split(separator)[:-1]
    for kv in keyvalue:
        if '=' in kv:
            k, v = kv.split('=', 1)
            if k in fields:
                message = re.sub(rf'{k}=[^{separator}]+',
                                 f'{k}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s \
%(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialize """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ custom format """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        record.msg = "; ".join(
            [kv.strip() for kv in record.msg.split(";") if kv.strip()]) + ";"
        return super().format(record)


def get_logger() -> logging.Logger:
    """ create logger named 'user_data'
    logger is like a note """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    """ return connector to db """
    from dotenv import load_dotenv
    load_dotenv()
    conn = connect(
        database=getenv('PERSONAL_DATA_DB_NAME'),
        host=getenv("PERSONAL_DATA_DB_HOST"),
        user=getenv('PERSONAL_DATA_DB_USERNAME'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD')
    )
    return conn


def main():
    """ main """
    logger = get_logger()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    for row in cursor:
        if len(row) == 8:
            name, email, phone, ssn, password, ip, last_login, user_agent = row
            message = f"name={name};email={email};phone={phone};\
ssn={ssn};password={password};ip={ip};last_login={last_login};\
user_agent={user_agent};"
            logger.info(message)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
