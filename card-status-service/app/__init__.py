### __init__.py ###

import logging

date_format = '%Y-%m-%d %H:%M:%S %z'
log_format = '[%(levelname)s][%(asctime)s] %(name)s:%(funcName)s: %(message)s'

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=date_format
)