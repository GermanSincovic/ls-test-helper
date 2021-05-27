import json
import os
import re
import time
from datetime import datetime

import paramiko

from modules import Log
from modules.Constants import RESULTS_DIR


def get_config():
    with open('modules/application.conf') as config_file:
        return json.load(config_file)


def connect(dns):
    Log.info("Connecting to {}".format(dns))
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(dns, username='ivan.didyk', key_filename='C:\\Users\\IDidyk\\.ssh\\id_rsa.ppk')
    except TimeoutError as error:
        Log.error(error)
        return str(error), 410
    else:
        return ssh


def date_time_search_limit(ssh, data, config):
    component = config[data['component']]
    path = component['folder_path']
    if 'dtl' in data.keys():
        stdin, stdout, stderr = ssh.exec_command("ls -A -c -r {} | grep .log".format(path))
        file_list = stdout.read().decode("cp1252")
        f = filter(None, file_list.split("\n"))
        files = list(f)
        string = ""
        current = ""
        for file in files:
            if "current" not in file:
                file_date = datetime.strptime(re.sub(r'\w+-(\d+)-(\d+)-(\d+)-(\d+)-\d+.log', r"\1/\2/\3 \4:00", file),
                                              "%Y/%m/%d %H:%M")
                edge_date = datetime.strptime(data['dtl'], "%Y-%m-%dT%H")
                if file_date >= edge_date:
                    string = " ".join([string, path + file])
            else:
                current = path + file
        string = " ".join([string, current])
    else:
        string = path + "*.log"
    return string


def get_result_file_name(data):
    endpoint = data['endpoint']
    result_filename = "{}_{}".format(data['component'], endpoint)
    for add in data['additional']:
        result_filename += "_" + add + "_" + data['additional'][add]
    result_filename += ".json"
    result_filename = result_filename.replace('/', '').replace(':', '')
    return result_filename


def get_cat_regex(data, config):
    component = config[data['component']]
    endpoint = data['endpoint']
    regex_pattern = component['endpoints'][endpoint]['regex']
    regex = regex_pattern
    for add in data['additional']:
        regex = regex.replace("{{" + add + "}}", data['additional'][add])
    return regex


def get_command(ssh, data, config):
    return "cat {} | grep -E '{}' > {}".format(date_time_search_limit(ssh, data, config),
                                               get_cat_regex(data, config),
                                               get_result_file_name(data))


def collect(data):
    # Preparation
    Log.info("Command preparation...")
    config = get_config()
    component = config[data['component']]
    file_name = get_result_file_name(data)
    ssh = connect(component['dns'])
    cat_command = get_command(ssh, data, config)

    # CAT operation
    Log.info("Command executing...")
    channel = ssh.get_transport().open_session()
    channel.exec_command(cat_command)
    while not channel.exit_status_ready():
        time.sleep(1)

    # Copying from remote to local
    Log.info("Try to copy remote file...")
    sftp = ssh.open_sftp()
    remote_path = "/home/ivan.didyk/{}".format(file_name)
    local_path = os.path.join(RESULTS_DIR, file_name)
    sftp.get(remote_path, local_path)

    # Remove remote file
    Log.info("Try to remove remote file...")
    sftp.remove(remote_path)
    sftp.close()
    Log.info("SFTP connection closed...")
    ssh.close()
    Log.info("SSH connection closed...")

    return get_result_file_name(data), 200
