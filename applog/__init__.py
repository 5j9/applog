import logging
import sys
from pathlib import Path
from re import compile as rc

COLORS = {
    'DEBUG': '\033[36m',
    'INFO': '\033[32m',
    'WARNING': '\033[33m',
    'ERROR': '\033[31m',
    'CRITICAL': '\033[35m',
    'RESET': '\033[0m',
    'GREEN': '\033[32m',
    'NUMBER': '\033[1;36m',  # Bold cyan for numbers
}

sub_numbers = rc(r'\b(\d+(?:\.\d+)?)\b').sub


class CustomFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)

        # Simple number highlighting
        message = sub_numbers(
            f'{COLORS["NUMBER"]}\\1{COLORS["RESET"]}',
            message,
        )

        time_str = self.formatTime(record, self.datefmt)
        file_path = Path(record.pathname).resolve()
        line_no = record.lineno
        url = f'file:///{file_path.as_posix()}#{line_no}'
        clickable_location = (
            f'\x1b]8;;{url}\x1b\\{record.funcName}\x1b]8;;\x1b\\'
        )
        level_color = COLORS.get(record.levelname, COLORS['RESET'])
        colored_level = f'{level_color}{record.levelname:8}{COLORS["RESET"]}'
        colored_time = f'{COLORS["GREEN"]}{time_str}{COLORS["RESET"]}'

        return f'{colored_time} | {colored_level} | {clickable_location}: {message}{COLORS["RESET"]}'


root_logger = logging.getLogger()
root_logger.handlers.clear()

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter(datefmt='%d %H:%M:%S'))

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
