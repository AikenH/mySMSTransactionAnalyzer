import os
from functools import wraps
import time
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler


def parse_date(date_str, current_year):
    """
    Parses a date string and returns a datetime object.
    Args:
        date_str (str): The date string to parse.
        current_year (int): The current year to use for parsing the date.
    Returns:
        datetime: The parsed datetime object.
    Raises:
        ValueError: If the date format is invalid.
    """
    try:
        return datetime.strptime(f"{current_year}-{date_str}", '%Y-%m月%d日')
    except ValueError:
        pass
    raise ValueError('Invalid date format')


# def setup_logger():
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s',
#         filename='app.log',
#         filemode='a'
#     )
#     return logging.getLogger(__name__)

def setup_logger():
    """
    Sets up the logger with basic configuration for logging.
    Logs are written to 'app.log' file in append mode with a maximum size and rotation.
    Returns:
        A configured logger instance.
    """
    # create a logger with the name of the module
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler that logs messages to a file with rotation
    log_dir = 'logs'
    log_file = 'app.log'
    log_path = os.path.join(log_dir, log_file)

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    handler = RotatingFileHandler(
        log_path, mode='a', maxBytes=5*1024*1024,
        backupCount=2, encoding='utf-8', delay=0
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    )

    # add the file handler to the logger
    logger.addHandler(handler)
    return logger


logger = setup_logger()


def log_execution(verbose=False):
    """
    Decorator for logging the execution time of a function.
    Args:
        verbose (bool): If True, the execution time is logged. Defaults to False.
    Returns:
        Decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            if verbose:
                logger.info(f"Executed {func.__name__} in {end_time - start_time:.4f} seconds")
            return result
        return wrapper
    return decorator
