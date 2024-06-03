
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from uuid import uuid4


def get_logger(name: str, log_to_file: bool = False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not os.path.exists(log_dir := f'./logs/{name.lower()}'):
        os.makedirs(log_dir)

    if log_to_file:
        uuid_ = str(uuid4()).split("_")
        handler: logging.Handler = TimedRotatingFileHandler(
            filename=f"{log_dir}/{name}_{uuid_}.log",
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8")
        handler.setLevel(logging.INFO)
    else:
        handler = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)
    logger.propagate = False  # Отключение распространения логов вверх по иерархии

    return logger