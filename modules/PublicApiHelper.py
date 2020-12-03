import requests

from modules import FileManager


def get_url_config():
    return FileManager.get_url_mapping_config()


def get_public_api_data_daily(environment, sport, date):
    config = get_url_config()
    public_api_daily_pattern = config[environment]['public-api-base-url'] + config[environment]['public-api-event-list']
    public_api_daily_link = public_api_daily_pattern.format(sport=sport, ls_date=date)
    # r = requests.get(public_api_daily_link)
    # public_api_daily_data =
    # return requests.get(public_api_daily_link).json()
    return requests.get(public_api_daily_link).json()


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
