import json
import os
import subprocess
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from modules import Log
from modules.Constants import RESULTS_DIR, MAIN_REPOSITORY_PATH, MODULES_DIR, BASE_FOLDER, ARCHIVE_DIR, LOGS_DIR, \
    UPLOAD_DIR


def __listdirattr(path):
    tmp = []
    for file in os.listdir(path):
        stats = os.stat(os.path.join(path, file))
        tmp.append({
            "name": file,
            "size": stats.st_size,
            "created": stats.st_ctime
        })
    return tmp


def get_application_config():
    with open('modules/application.conf') as config_file:
        return json.load(config_file), 200


def get_file(folder, filename):
    with open(os.path.join(MAIN_REPOSITORY_PATH, folder, filename)) as file:
        data = file.read()
    return data, 200


def search_files():
    result = []
    folders = os.listdir(MAIN_REPOSITORY_PATH)
    for folder in folders:
        path = os.path.join(MAIN_REPOSITORY_PATH, folder)
        result.append({
            "folder": folder,
            "path": path,
            "files": __listdirattr(path)
        })
    return result, 200


def delete_file(folder, filename):
    file = os.path.join(MAIN_REPOSITORY_PATH, folder, filename)
    if os.path.exists(file):
        os.remove(file)
        if not os.path.exists(file):
            Log.info("File {} is deleted".format(filename))
            return "File {} removed".format(filename), 200
        else:
            return "Something went wrong", 510
    else:
        return "Not found", 404


def move_file(old_folder, new_folder, filename):
    Log.info("Try to move {} from {} to {}".format(filename, old_folder, new_folder))
    old_path = os.path.join(MAIN_REPOSITORY_PATH, old_folder, filename)
    new_path = os.path.join(MAIN_REPOSITORY_PATH, new_folder, filename)
    if os.path.exists(old_path):
        if old_path == new_path:
            return "File is already in this folder", 400
        os.rename(old_path, new_path)
        if os.path.exists(new_path):
            return "File moved to /" + new_folder, 200
        else:
            return "Something went wrong", 510
    else:
        return "Not found", 404


def separate_file(folder, filename):
    Log.info("Separating file {}".format(filename))
    ps_path = 'powershell'
    separator_path = os.path.join(MODULES_DIR, 'separator.ps1')
    file = os.path.join(MAIN_REPOSITORY_PATH, folder, filename)
    command = ps_path + " -Command " + separator_path + " " + file
    result = subprocess.check_output(command).decode('cp866').rstrip()
    return result, 200


def get_timestamp():
    return datetime.datetime.now().timestamp()


def remove_old_result_files():
    Log.info("Checking RESULTS_DIR for old files")
    week = 604800  # seconds in 1 week
    res = list()
    for file in __listdirattr(RESULTS_DIR):
        if file['created'] < get_timestamp() - week:
            Log.info("File {} is older than 1 week. Deleting...".format(file['name']))
            delete_file(RESULTS_DIR, file['name'])
    return res, 200


def run_cleaner():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=remove_old_result_files, trigger="interval", hours=3)
    scheduler.start()
    Log.info("Cleaner running in background")


def check_dirs_existing():
    if not os.path.exists(MAIN_REPOSITORY_PATH):
        os.makedirs(MAIN_REPOSITORY_PATH)
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)


def get_log():
    with open('logs/app.log') as log:
        data = log.read()
        return data, 200
