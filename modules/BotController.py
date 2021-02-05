import json
import os

import requests

from modules import FileManager
from modules.Constants import MODULES_DIR


# TODO: Batch sending has to be done on server side, not client!
def get_chats_from_updates():
    chats = []
    url = "https://api.telegram.org/bot1555371617:AAGfvT8Bn_xpTSC2vqiz7BatuVuGiIQbWjo/getUpdates"
    data = requests.get(url=url).json()
    for n in data['result']:
        id = n['message']['chat']['id']
        if id > 0 and id not in chats:
            chats.append(id)
    return chats


def get_subscriptions_list():
    return FileManager.get_file(MODULES_DIR, "subscriptions.txt")[0]


def update_subscriptions_list():
    updates = get_chats_from_updates()
    subscriptions_cache = get_subscriptions_list()
    if not subscriptions_cache:
        subscriptions_cache = []
    else:
        subscriptions_cache = json.loads(subscriptions_cache)
    for ns in updates:
        if ns not in subscriptions_cache:
            subscriptions_cache.append(ns)
    FileManager.write_file(MODULES_DIR, "subscriptions.txt", json.dumps(subscriptions_cache))


def send_message_to_single_chat(chat_id, text):
    url = "https://api.telegram.org/bot1555371617:AAGfvT8Bn_xpTSC2vqiz7BatuVuGiIQbWjo/sendMessage"
    data = {
        "chat_id": chat_id,
        "parse_mode": "HTML",
        "text": text
    }
    requests.post(url=url, json=data)


def send_message_to_all_chats(text):
    text = text["text"]
    subscriptions_cache = get_subscriptions_list()
    if subscriptions_cache:
        subscriptions_cache = json.loads(subscriptions_cache)
    for chat_id in subscriptions_cache:
        send_message_to_single_chat(chat_id, text)


def check_subscriptions_cache_file_existence():
    if not os.path.exists(os.path.join(MODULES_DIR, "subscriptions.txt")):
        with open(os.path.join(MODULES_DIR, "subscriptions.txt"), 'w'):
            pass
