#!/usr/bin/env python3

"""
Module: filtered_logger.py
"""

import logging
import mysql.connector
import os
import re
from typing import List


# PII fields to be obscured
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    takes no arguments and returns a
    logging.Logger object named user_data.
    Only log up to logging.INFO level
    Propagate messages = False
    Use StreamHandler with RedactingFormatter
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Fetch database credentials using environment variables
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.environ.get("PERSONAL_DATA_DB_NAME")

    conn = mysql.connector.connect(user=username,
                                   password=password,
                                   host=host,
                                   database=database)

    return conn


def main():
    """
    obtain a database connection using get_db and
    retrieve all rows in the users table
    """
    # Set up logging
    logger = get_logger()

    # Establish db connection
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users")
    fields = [row[0] for row in cursor.description]

    for rows in cursor:
        msg = ''.join(f'{field}={str(row)};' for row,
                      field in zip(rows, fields))
        logger.info(msg.strip())

    # Close cursor & db connection
    cursor.close()
    db_conn.close()


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method for RedactingFormatter class
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records
        using filter_datum
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


if __name__ == "__main__":
    main()
