import logging

#getLogger() method takes the test case name as input
logger = logging.getLogger(__name__)
# setting the logger level
logger.setLevel(level=logging.INFO)
logger.debug("Debug log")
logger.info("Information log")
logger.warning("Warning log")
logger.error("Error log")
logger.critical("Critical log")
# Formatter() method takes care of the log file formatting
formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(filename)s::%(lineno)d::%(message)s")
#FileHandler() method takes location and path of log file
file_handler = logging.FileHandler("GP/reports_logs/GP_log.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
