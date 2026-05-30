__version__ = '1.0.1'
import logging
import os
import platform
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


def supports_emoji():
    """Determine if the terminal can display emoji"""
    if not sys.stdout.isatty():
        return False

    # Allow explicit override
    if os.environ.get('NO_EMOJI'):
        return False
    if os.environ.get('FORCE_EMOJI'):
        return True

    # VS Code terminal supports emoji
    if os.environ.get('TERM_PROGRAM') == 'vscode':
        return True

    # Windows legacy terminals are the main problem children
    if platform.system() == 'Windows':
        # Windows Terminal has WT_SESSION env var
        return bool(os.environ.get('WT_SESSION'))

    # Linux TTY consoles usually don't have emoji fonts
    if platform.system() != 'Windows' and not sys.stdout.isatty():
        term = os.environ.get('TERM', '').lower()
        if term == 'linux':
            return False

    # Assume true for everything else (macOS, modern Linux, etc.)
    return True


class ColorFormatter(logging.Formatter):
    """Formatter with colors, hyperlinks, and emojis"""

    # Map log levels to emojis (emoji-only mode)
    LEVEL_EMOJIS = {
        'DEBUG': '🐛',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🔥',
    }

    # Fallback text for terminals without emoji support
    LEVEL_FALLBACK = {
        'DEBUG': 'DBG',
        'INFO': 'INF',
        'WARNING': 'WRN',
        'ERROR': 'ERR',
        'CRITICAL': 'CRT',
    }

    def __init__(self, *args, use_emoji=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_emoji = use_emoji

    def format(self, record):
        message = super().format(record)
        message = sub_numbers(f'{Color.NUMBER}\\1{Color.RESET}', message)

        time_str = self.formatTime(record, self.datefmt)
        line_no = record.lineno
        url = f'{Path(record.pathname).as_uri()}#{line_no}'
        clickable_location = (
            f'\x1b]8;;{url}\x1b\\{record.funcName}\x1b]8;;\x1b\\'
        )

        # Use emoji or fallback text
        if self.use_emoji:
            level_symbol = self.LEVEL_EMOJIS.get(record.levelname, '•')
            colored_level = f'{Color.GREEN}{level_symbol}{Color.RESET}'
        else:
            level_text = (
                self.LEVEL_FALLBACK.get(record.levelname)
                or record.levelname[:3]
            )
            level_color = getattr(Color, record.levelname, Color.RESET)
            colored_level = f'{level_color}{level_text:3}{Color.RESET}'

        colored_time = f'{Color.GREEN}{time_str}{Color.RESET}'

        return f'{colored_time} {colored_level} {clickable_location}: {message}{Color.RESET}'


class PlainFormatter(logging.Formatter):
    """Plain text formatter without colors or hyperlinks"""

    LEVEL_EMOJIS = {
        'DEBUG': '🐛',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '💀',
    }

    LEVEL_FALLBACK = {
        'DEBUG': 'DBG',
        'INFO': 'INF',
        'WARNING': 'WRN',
        'ERROR': 'ERR',
        'CRITICAL': 'CRT',
    }

    def __init__(self, *args, use_emoji=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_emoji = use_emoji

    def format(self, record):
        message = super().format(record)
        time_str = self.formatTime(record, self.datefmt)

        if self.use_emoji:
            level_symbol = self.LEVEL_EMOJIS.get(record.levelname, '•')
            return f'{time_str} {level_symbol} {record.funcName}:{record.lineno} - {message}'
        else:
            level_text = self.LEVEL_FALLBACK.get(
                record.levelname, record.levelname[:3]
            )
            return f'{time_str} {level_text:3} {record.funcName}:{record.lineno} - {message}'


# Determine emoji support
USE_COLORS = (
    not os.environ.get('NO_COLOR')  # Disable if NO_COLOR is set
    and (os.environ.get('FORCE_COLOR') or sys.stdout.isatty())
)

USE_EMOJI = supports_emoji()

# Choose formatter
if USE_COLORS:
    formatter = ColorFormatter(datefmt='%a %H:%M:%S', use_emoji=USE_EMOJI)
else:
    formatter = PlainFormatter(datefmt='%a %H:%M:%S', use_emoji=USE_EMOJI)


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
