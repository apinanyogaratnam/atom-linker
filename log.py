import logging
import os

log_level_str = os.environ.get('LOG_LEVEL', 'DEBUG')
log_level = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}.get(log_level_str, logging.DEBUG)


def get_logger(file: str, level: int = log_level) -> logging.Logger:
    """Get a logger instance.

    Args:
    ----
        file (str): The file name to create the logger for.
        level (int): The logging level to set the logger to.

    Returns:
    -------
        logging.Logger: A logger instance.
    """
    file_name = os.path.basename(file)
    logger = logging.getLogger(file_name)

    # Setup logger to write to file
    fh = logging.FileHandler(f"logs/{file_name}.log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    # Ensure logger is set to debug level, so it logs messages of DEBUG and above.
    logger.setLevel(level)

    return logger
