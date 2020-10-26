import logging
import os

from modules.Constants import BASE_FOLDER


def log_config():
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(BASE_FOLDER, "logs", "app.log"), filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s')


def debug(string):
    log_config()
    logging.debug(string)


def info(string):
    log_config()
    logging.info(string)


def warning(string):
    log_config()
    logging.warning(string)


def error(string):
    log_config()
    logging.error(string)


def critical(string):
    log_config()
    logging.critical(string)
