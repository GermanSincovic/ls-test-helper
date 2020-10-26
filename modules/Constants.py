import os

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAIN_REPOSITORY_PATH = os.path.join(BASE_FOLDER, "files")

RESULTS_DIR = os.path.join(MAIN_REPOSITORY_PATH, "results")

ARCHIVE_DIR = os.path.join(MAIN_REPOSITORY_PATH, "archive")

MODULES_DIR = os.path.join(BASE_FOLDER, "modules")

MAINTENANCE = False
