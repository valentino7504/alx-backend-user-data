#!/usr/bin/env python3
'''

Filtered logger

'''
import logging
import re
from typing import List


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
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''format method'''
        sep = self.SEPARATOR
        msg = filter_datum(self.__fields, self.REDACTION, record.msg, sep)
        record.msg = msg
        return super().format(record)
