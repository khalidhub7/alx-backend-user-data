#!/usr/bin/env python3
"""
Mask sensitive data in log messages
and log user data from a database.
"""
import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Mask specified fields in a log message.
    Returns:
        str: The masked log message.
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Formatter class for redacting sensitive information"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redacts the sensitive fields in the log record message.
        Returns:
            str: The formatted and redacted log message.
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates and configures a logger instance"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    h = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    h.setFormatter(formatter)

    logger.addHandler(h)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Establishes and returns a connection to the database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(user=user, password=passwd,
                                   host=host, database=db_name)


def main():
    """Func to fetch user data from the DB and log it"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names

    for u in cursor:
        message = "".join(f"{i}={v}; " for i, v in zip(fields, u))
        logger.info(message.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
