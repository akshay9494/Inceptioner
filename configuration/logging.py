import logging
from logging import handlers
from datetime import datetime
from .instance import config
import os

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -10s %(funcName) -20s %(lineno) -5d: %(message)s')
log_name = 'logs_{}.log'.format(datetime.now().strftime('%Y-%m-%d--%H-%M-%S'))

handler = handlers.RotatingFileHandler(os.path.join(config.log_dir, log_name), maxBytes=100000, backupCount=100)

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[
        handler
    ]
)