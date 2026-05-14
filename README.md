# applog

A beautiful, zero-dependency logging formatter for Python with colors, clickable file links, and intelligent number highlighting.

## Features

- 🎨 **Colored output** by log level (respects `NO_COLOR` and `FORCE_COLOR` standards)
- 🔗 **Clickable file links** (OSC 8 hyperlinks) - Ctrl+Click to open in your editor
- 🔢 **Automatic number highlighting** - numbers stand out in your logs
- 📦 **Zero external dependencies** - pure Python standard library
- 🚀 **No pre-rendering** - logs wrap correctly when terminal resizes
- ⚙️ **Environment variable aware** - follows `NO_COLOR`, `FORCE_COLOR` conventions

## Installation

``uv add applog``

## Quick Start
```python
from applog import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

Output (imagine this with colors, since github does not allow colors):
```
Thu 12:42:25 | DEBUG    | <module>: Debug message
Thu 12:42:26 | INFO     | <module>: Info message
Thu 12:42:26 | WARNING  | <module>: Warning message
Thu 12:42:26 | ERROR    | <module>: Error message
Thu 12:42:26 | CRITICAL | <module>: Critical message
```

## Changing Date Format
```python
from applog import root_logger

# Change to 24-hour time without seconds
root_logger.handlers[0].formatter.datefmt = '%H:%M'

# Change to full datetime
root_logger.handlers[0].formatter.datefmt = '%Y-%m-%d %H:%M:%S'
```


## Customizing Colors
```python
from applog import Color, root_logger

# Modify color codes (ANSI escape sequences)
Color.INFO = '\033[94m'  # Bright blue for INFO
```

## Using with Standard Logging
``applog`` configures the root logger, so any standard logging calls will use the same formatting:

```python
import logging
from applog import logger

# These will all have the same beautiful formatting
logging.warning("Root logger warning")
custom_logger = logging.getLogger(__name__)
custom_logger.info("Custom logger info")
```


## Advanced Usage
### Adding Handlers
```python
from applog import root_logger
import logging

# Add file handler
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
root_logger.addHandler(file_handler)
```

### Creating Child Loggers
```python
from applog import logger

module_logger = logger.getChild('module_name')
module_logger.info("This will inherit parent settings")
```

## Notes
- The module configures the root logger on import - import it early in your application.
- Hyperlinks use OSC 8 sequences - won't work in very old terminals


## Why applog?
- **vs rich.logging:** Logs adapt when you resize your terminal (no pre-rendering)
- **vs loguru:** Works with all standard `logging` calls out of the box
- **The result:** Beautiful, clickable, dependency-free logging that just works
