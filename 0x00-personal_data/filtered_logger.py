#!/usr/bin/env python3
'''

Filtered logger

'''
import logging
import os
import re
from typing import List

import mysql.connector

PII_FIELDS = ('name', 'email', 'ssn', 'phone', 'password')


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    '''filters the log lines'''
    pattern = rf'(\b(?:{"|".join(fields)})\b)=[^ {separator}]*'
    return re.sub(pattern, lambda match: f'{match.group(1)}={redaction}',
                  message)


class RedactingFormatter(logging.Formatter):
    '''Redacting Formatter class'''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''format method'''
        sep = self.SEPARATOR
        msg = filter_datum(self.__fields, self.REDACTION, record.msg, sep)
        record.msg = msg
        return super().format(record)


def get_logger(self) -> logging.Logger:
    '''returns a suitable logger'''
    logger = logging.getLogger(name="user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''returns an SQL connection'''
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    cnx = mysql.connector.connection.MySQLConnection(
        host=host,
        user=username,
        password=pwd,
        database=db_name
    )
    return cnx
