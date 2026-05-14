import logging
import sys
from pathlib import Path

# ANSI color codes
COLORS = {
    'DEBUG': '\033[36m',  # Cyan
    'INFO': '\033[32m',  # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',  # Red
    'CRITICAL': '\033[35m',  # Magenta
    'RESET': '\033[0m',
    'GREEN': '\033[32m',  # For time stamp
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Get the original message
        message = super().format(record)

        # Format time
        time_str = self.formatTime(record, self.datefmt)

        # Create clickable link for file and line
        file_path = Path(record.pathname).resolve()
        line_no = record.lineno
        url = f'file:///{file_path.as_posix()}#{line_no}'

        # OSC 8 hyperlink
        clickable_location = (
            f'\x1b]8;;{url}\x1b\\{record.funcName}\x1b]8;;\x1b\\'
        )

        # Apply colors
        level_color = COLORS.get(record.levelname, COLORS['RESET'])
        colored_level = f'{level_color}{record.levelname:8}{COLORS["RESET"]}'
        colored_time = f'{COLORS["GREEN"]}{time_str}{COLORS["RESET"]}'

        # Format the final output
        return f'{colored_time} | {colored_level} | {clickable_location}: {level_color}{message}{COLORS["RESET"]}'


# Configure the ROOT logger (not logger named __name__)
root_logger = logging.getLogger()  # This gets the root logger

# Remove any existing handlers
root_logger.handlers.clear()

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Create formatter and add to handler
formatter = CustomFormatter(datefmt='%d %H:%M:%S')
console_handler.setFormatter(formatter)

# Add handler to root logger
root_logger.addHandler(console_handler)


logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
