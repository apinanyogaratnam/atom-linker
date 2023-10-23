from log import get_logger

logger = get_logger(__file__)


class StatsType:
    THREADS = "threads"


if __name__ == "__main__":
    logger.debug(StatsType.THREADS)
