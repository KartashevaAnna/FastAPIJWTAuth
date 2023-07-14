import logging
import sys

from loguru import logger


class LoguruHandler(logging.Handler):
    """Handler transmitting messages from logging to loguru."""

    def init(self):
        super().init()

    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.file:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(logg, level: str = "ERROR"):
    logg.remove()
    logging.root.handlers = [LoguruHandler()]
    logging.root.setLevel(level.upper())

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logg.add(
        sys.stderr,
        level=level.upper(),
        format="<level>{level}</level> | <green>{time:YYYY-MM-DD HH:mm:ss Z}</green> | {module} | {message}",
        colorize=True,
        enqueue=True,
        backtrace=True,
    )
    for name in [
        *logging.root.manager.loggerDict.keys(),  # type: ignore
        "uvicorn",
        "uvicorn.error",
        "uvicorn.server",
        "fastapi",
        "sqlalchemy",
    ]:
        logging.getLogger(name).handlers = []
    return logg
