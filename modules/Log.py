import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from modules.Constants import BASE_FOLDER

filepath = os.path.join(BASE_FOLDER, "logs")


class LiveScoreRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, basedir, log_file_name, max_bytes=500 * 1024, backup_count=10):
        self.current_part_ = 'current'
        self.extension_ = 'log'

        self.log_file_name_ = log_file_name + '-' + self.current_part_ + '.' + self.extension_
        self.basedir_ = basedir

        self.baseFilename = os.path.join(self.basedir_, self.log_file_name_)

        logging.handlers.RotatingFileHandler.__init__(self, self.baseFilename,
                                                      maxBytes=max_bytes, backupCount=backup_count)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:
            existing_files = list(f for f in os.listdir(self.basedir_) if os.path.isfile(os.path.join(self.basedir_, f)) \
                                  and f.endswith(".{}".format(self.extension_)))

            existing_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.basedir_, f)))

            existing_files_count = len(existing_files)
            if existing_files_count >= self.backupCount:
                for file in existing_files[0: existing_files_count - self.backupCount - 1]:
                    abs_file = os.path.abspath(os.path.join(self.basedir_, file))
                    if os.path.exists(abs_file):
                        os.remove(abs_file)

        dynamic_part = '{:%Y-%m-%d-%H-%M}'.format(datetime.now())
        new_file_name = self.baseFilename.replace(self.current_part_, dynamic_part)
        self.rotate(self.baseFilename, new_file_name)

        if self.backupCount > 0:
            for root, dirs, files in os.walk(self.basedir_, topdown=False):
                existing_files = list(f if f.endswith(".{}".format(self.extension_)) else None for f in files)
                existing_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.basedir_, f)))

                for ef in existing_files[0: len(existing_files) - self.backupCount - 1]:
                    absef = os.path.abspath(os.path.join(self.basedir_, ef))
                    if os.path.exists(absef):
                        os.remove(absef)

        if not self.delay:
            self.stream = self._open()


def create_rotating_log():
    logging.basicConfig(
        handlers=[LiveScoreRotatingFileHandler(filepath, "app")],
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
