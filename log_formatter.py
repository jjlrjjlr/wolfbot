#!/bin/python3
# Log Formatter
# =======
# Custom log formatter for colored and markdown logging.
#
# Copyright 2021  jjlrjjlr (https://github.com/jjlrjjlr)

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------

import logging
from datetime import datetime
from os import path, makedirs

_TODAY = datetime.now().today().strftime('%Y-%m-%d')


class ColoredFormatter(logging.Formatter):
    '''
    Logging formatter that provides colored output for terminals.
    '''
    FMT = '({asctime}) {module} [{levelname:^9}]: {message}'
    FORMATS = {
        logging.DEBUG: f'\33[38;5;243m{FMT}\33[0m',
        logging.INFO: f'\33[32;5;215m{FMT}\33[0m',
        logging.WARNING: f'\33[33;1m{FMT}\33[0m',
        logging.ERROR: f'\33[31;5m{FMT}\33[0m',
        logging.CRITICAL: f'\33[31;2m{FMT}\33[0m'
    }
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)


class MarkdownFormatter(logging.Formatter):
    '''
    Logging formatter that provides colored output as markdown.
    '''
    FMT = '({asctime}) {module} [{levelname:^9}]: {message}'
    FORMATS = {
        logging.DEBUG: f'<p style="color:grey">{FMT}</p>',
        logging.INFO: f'<p style="color:green">{FMT}</p>',
        logging.WARNING: f'<p style="color:yellow">{FMT}</p>',
        logging.ERROR: f'<p style="color:red">{FMT}</p>',
        logging.CRITICAL: f'<p style="color:darkred">{FMT}</p>'
    }
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)


def color_handler() -> logging.StreamHandler:
    _handler = logging.StreamHandler()
    _handler.setFormatter(ColoredFormatter())
    return _handler

def markdown_handler(filename: str=f'{_TODAY}.md', dir_path: str='.') -> logging.FileHandler:
    makedirs(dir_path, exist_ok=True)
    _handler = logging.FileHandler('/'.join([dir_path, filename]))
    _handler.setFormatter(MarkdownFormatter())
    return _handler

def tests() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[color_handler(), markdown_handler(dir_path='./tests')]
    )
    logging.debug('This test debug message.')
    logging.info('This is a test info message.')
    logging.warning('This is a test warning.')
    logging.error('This is a test error.')
    logging.critical('This is a test critical message.')

if __name__ == '__main__':
    tests()