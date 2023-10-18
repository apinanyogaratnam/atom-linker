import logging
import os
import inspect


class LoggerProxy:
    def __getattr__(self, name):
        # Dynamically determine the logger based on the calling module
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        file_name = os.path.basename(filename)

        logger = logging.getLogger(file_name)

        # Configure the logger if it hasn't been configured before
        if not logger.hasHandlers():
            if not os.path.exists("logs"):
                os.makedirs("logs")
            fh = logging.FileHandler(f"logs/{file_name}.log")
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            fh.setFormatter(formatter)
            logger.setLevel(logging.DEBUG)

        # Delegate attribute access to the logger
        return getattr(logger, name)


logger = LoggerProxy()

# NOTE: this is how you call it
if __name__ == '__main__':
    from dynamic_instantiated_logger import logger

    logger.debug("This is a debug message")
