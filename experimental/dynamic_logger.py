import logging
import os
import inspect


def get_logger(level: int = logging.DEBUG) -> logging.Logger:
    """Get a logger instance.

    Args:
    ----
        level (int): The logging level to set the logger to.

    Returns:
    -------
        logging.Logger: A logger instance.
    """
    # Get the name of the file that called this function
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    file_name = os.path.basename(filename)

    logger = logging.getLogger(file_name)

    # Setup logger to write to file
    if not os.path.exists("logs"):
        os.makedirs("logs")
    fh = logging.FileHandler(f"logs/{file_name}.log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    # Ensure logger is set to debug level, so it logs messages of DEBUG and above.
    logger.setLevel(level)

    return logger


# NOTE: this is how you call it
if __name__ == "__main__":
    from log import get_logger
    logger = get_logger()
