import json
import os

import requests
from lxml import html

from modules import Log, FileManager, BotController
from modules.Constants import MODULES_DIR


def get_health_pages():
    old_health_data = FileManager.get_file(MODULES_DIR, "health_page_cache.txt")[0]
    old_health_data = json.loads(old_health_data)

    devtest_url = "http://ls-tools-ls-g.dev-i.net:8091/health-status/"
    preprod_url = "https://preprod-component-monitoring.livescore.com/health-status/"
    prod_url = "https://component-monitoring.livescore.com/health-status/"
    loadtest_url = "http://35.246.114.214:8091/health-status/"
    loadtest_iron_url = "http://35.246.114.214:8092/health-status/"
    sr_keys_url = "http://ls-tools-ls-g.dev-i.net:8060/"

    health_data = []

    try:
        devtest = requests.get(devtest_url).json()
        for env in devtest:
            health_data.append({env: devtest[env]})
    except Exception as e:
        Log.warning("Can't get data from {}, {}".format(devtest_url, e))

    try:
        preprod = requests.get(preprod_url).json()
        for env in preprod:
            health_data.append({env: preprod[env]})
    except Exception as e:
        Log.warning("Can't get data from {}, {}".format(preprod_url, e))

    try:
        prod = requests.get(prod_url).json()
        for env in prod:
            health_data.append({env: prod[env]})
    except Exception as e:
        Log.warning("Can't get data from {}, {}".format(prod_url, e))

    try:
        loadtest = requests.get(loadtest_url).json()
        for env in loadtest:
            health_data.append({env: loadtest[env]})
    except Exception as e:
        Log.warning("Can't get data from {}, {}".format(loadtest_url, e))

    try:
        loadtest_iron = {"loadtest-iron": requests.get(loadtest_iron_url).json()['loadtest']}
        for env in loadtest_iron:
            health_data.append({env: loadtest_iron[env]})
    except Exception as e:
        Log.warning("Can't get data from {}, {}".format(loadtest_iron_url, e))

    try:
        tree = html.fromstring(requests.get(sr_keys_url).content)
        headers = list()
        lines = list()
        sr_keys = {"sr-keys": []}
        for header in tree.xpath("//th/text()"):
            headers.append(header)
        for line in tree.xpath("//td/*/text()"):
            lines.append(line)
        for i in range(0, len(lines)):
            if len(sr_keys["sr-keys"]) < i // len(headers) + 1:
                sr_keys["sr-keys"].append({})
            sr_keys["sr-keys"][i // len(headers)].update({headers[i % len(headers)]: lines[i]})
        health_data.append(sr_keys)
    except Exception as e:
        Log.warning("Can't get data from {}, {}".format(sr_keys_url, e))

    if not os.path.exists(os.path.join(MODULES_DIR, "health_page_cache.txt")):
        with open(os.path.join(MODULES_DIR, "health_page_cache.txt"), 'w'):
            pass
    else:
        FileManager.write_file(MODULES_DIR, "health_page_cache.txt", json.dumps(health_data))

    msg_tpl = "Version changed!"
    change_list = ""

    for elem in range(len(health_data)):
        env = list(health_data[elem])[0]
        for el in range(len(health_data[elem][env])):
            try:
                if health_data[elem][env][el]["version"] != old_health_data[elem][env][el]["version"]:
                    change_list += "\n" + str.upper(env) + " - " + health_data[elem][env][el]["component"] + " - " + health_data[elem][env][el]["version"]
            except KeyError:
                pass

    if change_list:
        BotController.send_message_to_all_chats(msg_tpl + change_list)

    return health_data, 200
