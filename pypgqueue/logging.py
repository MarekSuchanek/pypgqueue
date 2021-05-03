import logging
import sys

from pypgqueue.consts import LOGGER_NAME

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)8s | %(module)s: %(message)s',
)
logger = logging.getLogger(LOGGER_NAME)
