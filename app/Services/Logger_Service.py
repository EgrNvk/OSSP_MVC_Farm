import logging
from pathlib import Path

HOME_DIR = Path.home()
DOCS_DIR = HOME_DIR / "Documents"
LOGS_DIR = DOCS_DIR / "OSSP_MVC_Farm_logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / "OSSP_MVC_Farm.log"

logger = logging.getLogger("OSSP_MVC_Farm")
logger.setLevel(logging.DEBUG)

logger.handlers.clear()
logger.propagate = False

FORMATTER = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(FORMATTER)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(FORMATTER)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info(f"Логи пишуться у: {LOG_FILE}")