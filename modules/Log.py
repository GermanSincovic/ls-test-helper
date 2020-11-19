import logging
import os
from logging.handlers import RotatingFileHandler

from modules.Constants import BASE_FOLDER

filepath = os.path.join(BASE_FOLDER, "logs", "app-current.log")


def create_rotating_log():
    logging.basicConfig(
        handlers=[RotatingFileHandler(filepath, maxBytes=100000, backupCount=10)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')


def debug(string):
    create_rotating_log()
    logging.debug(string)


def info(string):
    create_rotating_log()
    logging.info(string)


def warning(string):
    create_rotating_log()
    logging.warning(string)


def error(string):
    create_rotating_log()
    logging.error(string)


def critical(string):
    create_rotating_log()
    logging.critical(string)
