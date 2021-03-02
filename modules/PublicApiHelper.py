import json
import re

import requests

from modules import FileManager, Kafka, Log
from modules.Constants import FEATURE_NAMES, SPORT_NAMES


def get_url_config():
    return FileManager.get_url_mapping_config()


def get_sport_id_by_name(sn):
    for sport_id, sport_name in SPORT_NAMES.items():
        if sport_name == sn:
            return int(sport_id)


def find_priority_rules(mt, sport, stage):
    rules = {}
    for feature in mt:
        if "sportId" in feature \
                and feature["sportId"] == sport \
                and "tournamentStageId" not in feature:
            rules.update({FEATURE_NAMES[str(feature["featureId"])]: feature["providers"][0]["name"]})
    for feature in mt:
        if "sportId" in feature \
                and feature["sportId"] == sport \
                and "tournamentStageId" in feature \
                and feature["tournamentStageId"] == stage:
            rules.update({FEATURE_NAMES[str(feature["featureId"])]: feature["providers"][0]["name"]})
    return rules


def get_public_api_live_count(environment):
    config = get_url_config()
    public_api_live_count_link = config[environment]['public-api-base-url'] + config[environment][
        'public-api-live-counter']
    try:
        live_count = requests.get(public_api_live_count_link).json()
    except Exception as e:
        return "Internal Server Error", 500
    return live_count, 200


def get_freeze_list(environment):
    if environment in ["dev", "test"]:
        ids = []
        freezelistdata = requests.get("http://" + environment + "-crawler-enetapi-0-lsm.ls-g.net:8070/simulator/listfrozen").json()
        for el in freezelistdata:
            id_search = re.search(r"etails\D+(\d+)", el)
            if id_search:
                ids.append(id_search.group(1))
        return ids
    else:
        return []


def get_public_api_data_daily(environment, sport, date):
    freeze_list = get_freeze_list(environment)
    config = get_url_config()
    public_api_daily_pattern = config[environment]['public-api-base-url'] + config[environment]['public-api-event-list']
    public_api_daily_link = public_api_daily_pattern.format(sport=sport, ls_date=date)

    try:
        daily = requests.get(public_api_daily_link).json()
    except Exception as e:
        return "Internal Server Error", 500
    mapping_template_entry = requests.get(config[environment]['mapping-template-base-url'] + "/manifest.json")
    if mapping_template_entry.status_code == 200:
        mapping_template_entry = mapping_template_entry.json()["entries"][0]
        mapping_template = \
            requests.get(config[environment]['mapping-template-base-url'] + mapping_template_entry).json()[
                "featureProviders"]
    else:
        Log.warning("No mapping templates in Bucket Storage. Consuming from Kafka ({})".format(environment))
        mapping_template = Kafka.consume(environment, "export-mapping-template")
        mapping_template = json.loads(mapping_template[0])
        mapping_template = mapping_template["featureProviders"]

    full_daily = {"Stages": []}
    for stage in daily["Stages"]:
        stage["_LC"] = 0
        for event in stage["Events"]:
            if event["Epr"] == 1:
                stage["_LC"] += 1
            if True in (a in freeze_list for a in event["Pids"].values()):
                event["_FR"] = "1"
        stage["_FP"] = {}
        stage["_FP"].update(find_priority_rules(mapping_template, get_sport_id_by_name(sport), int(stage["Sid"])))
        stage["_FP_unique"] = []
        stage["_FP_unique"] = list(set(stage["_FP"].values()))
        full_daily["Stages"].append(stage)
    return full_daily


def get_public_api_data_event(environment, sport, id, pid):

    # for old API URL
    if sport == "hockey":
        sport = "ice_hockey"
    # eof

    config = get_url_config()
    composite_id = pid + "-" + id
    public_api_event_pattern = config[environment]['public-api-base-url'] + config[environment][
        'public-api-test-ui-event']
    public_api_event_link = public_api_event_pattern.format(sport=sport, composite_id=composite_id)
    try:
        event = requests.get(public_api_event_link).json()
    except ConnectionError as e:
        return "Internal Server Error", 500
    return event


def get_public_api_data(environment, feed, sport, date=None, id=None, pid=None):
    if feed == 'event-list' and sport and date:
        return get_public_api_data_daily(environment, sport, date), 200
    elif feed == 'event' and sport and id and pid:
        return get_public_api_data_event(environment, sport, id, pid), 200
    else:
        return "Bad request", 400
