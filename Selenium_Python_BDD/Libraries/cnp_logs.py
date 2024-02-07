import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler


ENV = os.environ.get("SPARC_SERVICE_NAME", None)
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
# LOG_FILE = ENV + "/automation_test/" + ENV + "_ui_tests.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    pass
    # file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    # file_handler.setFormatter(FORMATTER)
    # return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)
    logger.debug("Debug log")
    logger.info("Information log")
    logger.warning("Warning log")
    logger.error("Error log")
    logger.critical("Critical log")

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False

    return logger
