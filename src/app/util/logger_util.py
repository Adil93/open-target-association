import logging
import sys


def setup():

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s',
                                      datefmt='%d/%m/%Y %H:%M:%S')
    logFile = 'loader.log'
    # Setup File handler
    file_handler = logging.FileHandler(logFile)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Setup Stream Handler (i.e. console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.DEBUG)

    # Get our logger
    app_log = logging.getLogger()
    app_log.setLevel(logging.INFO)

    # Add both Handlers
    app_log.addHandler(file_handler)
    app_log.addHandler(stream_handler)
