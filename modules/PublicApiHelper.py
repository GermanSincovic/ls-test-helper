import requests

from modules import FileManager
from modules.Constants import FEATURE_NAMES, SPORT_NAMES


def get_url_config():
    return FileManager.get_url_mapping_config()


def get_sport_id_by_name(sn):
    for sport_id, sport_name in SPORT_NAMES.items():
        if sport_name == sn:
            return int(sport_id)


def find_priority_rules(mt, sport, stage):
    rules = {}
    for f in mt:
        if "sportId" in f \
                and f["sportId"] == sport \
                and "tournamentStageId" in f \
                and f["tournamentStageId"] == stage:
            rules.update({FEATURE_NAMES[str(f["featureId"])]: f["providers"][0]["name"]})
    if len(rules) < len(FEATURE_NAMES):
        for f in mt:
            if "sportId" in f \
                    and f["sportId"] == sport \
                    and "tournamentStageId" not in f:
                rules.update({FEATURE_NAMES[str(f["featureId"])]: f["providers"][0]["name"]})
    return rules


def get_public_api_data_daily(environment, sport, date):
    config = get_url_config()
    public_api_daily_pattern = config[environment]['public-api-base-url'] + config[environment]['public-api-event-list']
    public_api_daily_link = public_api_daily_pattern.format(sport=sport, ls_date=date)
    daily = requests.get(public_api_daily_link).json()
    mapping_template_entry = requests.get(config[environment]['mapping-template-base-url'] + "/manifest.json").json()["entries"][0]
    mapping_template = requests.get(config[environment]['mapping-template-base-url'] + mapping_template_entry).json()["featureProviders"]
    full_daily = {"Stages": []}
    for stage in daily["Stages"]:
        stage["_FP"] = {}
        stage["_FP"].update(find_priority_rules(mapping_template, get_sport_id_by_name(sport), int(stage["Sid"])))
        full_daily["Stages"].append(stage)
    return full_daily


def get_public_api_data_event(environment, sport, id):
    config = get_url_config()
    public_api_event_pattern = config[environment]['public-api-base-url'] + config[environment]['public-api-event']
    public_api_event_link = public_api_event_pattern.format(sport=sport, event_id=id)

    # v1/api/app/match/{sport}/{event_id}/2.0
    return requests.get(public_api_event_link).json()


def get_public_api_data(environment, feed, sport, date=None, id=None):
    if feed == 'event-list' and sport and date:
        return get_public_api_data_daily(environment, sport, date), 200
    elif feed == 'event' and sport and id:
        return get_public_api_data_event(environment, sport, id), 200
    else:
        return "Bad request", 400
