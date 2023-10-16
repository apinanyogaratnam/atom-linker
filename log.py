import logging
import os


def get_logger(file: str, level: int = logging.DEBUG) -> logging.Logger:
    """Get a logger instance.

    Args:
    ----
        file_name (str): The name of the file that the logger will write to.

    Returns:
    -------
        logging.Logger: A logger instance.
    """
    file_name = os.path.basename(file)
    logger = logging.getLogger(file_name)

    # Setup logger to write to file
    fh = logging.FileHandler(f"{file_name}.log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    # Ensure logger is set to debug level, so it logs messages of DEBUG and above.
    logger.setLevel(level)

    return logger
