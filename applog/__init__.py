__version__ = '1.0.0'
import logging
import os
import sys
from enum import StrEnum
from pathlib import Path
from re import compile as rc


class Color(StrEnum):
    """ANSI color codes for terminal output"""

    DEBUG = '\033[36m'
    INFO = '\033[32m'
    WARNING = '\033[33m'
    ERROR = '\033[31m'
    CRITICAL = '\033[35m'
    RESET = '\033[0m'
    GREEN = '\033[32m'
    NUMBER = '\033[1;36m'


sub_numbers = rc(r'\b(\d+(?:\.\d+)?)\b').sub


class ColorFormatter(logging.Formatter):
    """Formatter with colors and hyperlinks"""

    def format(self, record):
        message = super().format(record)
        message = sub_numbers(f'{Color.NUMBER}\\1{Color.RESET}', message)

        time_str = self.formatTime(record, self.datefmt)
        line_no = record.lineno
        url = f'{Path(record.pathname).as_uri()}#{line_no}'
        clickable_location = (
            f'\x1b]8;;{url}\x1b\\{record.funcName}\x1b]8;;\x1b\\'
        )

        level_color = getattr(Color, record.levelname, Color.RESET)
        colored_level = f'{level_color}{record.levelname:8}{Color.RESET}'
        colored_time = f'{Color.GREEN}{time_str}{Color.RESET}'

        return f'{colored_time} | {colored_level} | {clickable_location}: {message}{Color.RESET}'


class PlainFormatter(logging.Formatter):
    """Plain text formatter without colors or hyperlinks"""

    def format(self, record):
        message = super().format(record)
        time_str = self.formatTime(record, self.datefmt)
        return f'{time_str} | {record.levelname:8} | {record.funcName}:{record.lineno} - {message}'


USE_COLORS = (
    not os.environ.get('NO_COLOR')  # Disable if NO_COLOR is set
    and (os.environ.get('FORCE_COLOR') or sys.stdout.isatty())
)

if USE_COLORS:
    formatter = ColorFormatter(datefmt='%a %H:%M:%S')
else:
    formatter = PlainFormatter(datefmt='%a %H:%M:%S')


# Configure logger
root_logger = logging.getLogger()
root_logger.handlers.clear()

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

root_logger.addHandler(console_handler)
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


# Test with various message types
if __name__ == '__main__':
    logger.debug(f'Numbers like {42} and {3.14159} and hex {0xFF}')
    logger.info('Strings like \'hello\' and "world"')
    logger.warning(f"Lists: {[1, 2, 3]}, Dicts: {{'a': 1, 'b': 2}}")
    logger.error(f'{list(range(200))}')
    logger.critical(f'Boolean: {True}, None: {None}')
