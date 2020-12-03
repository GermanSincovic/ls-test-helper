import requests

_mt = requests.get("https://storage.googleapis.com/mta-dev/mapping_templates_1/2020/12/03/20-30-02/0.json").json()[
    "featureProviders"]
_sport = 1
_stage = 941


def find_priority_rules(mt, sport, stage):
    feature_names = {
        "1": "venue",
        "2": "goal scorers",
        "3": "goal assists",
        "4": "cards",
        "5": "head to head",
        "6": "spectators",
        "7": "incidents",
        "8": "line-ups",
        "9": "commentaries",
        "10": "referee",
        "11": "league table",
        "12": "stats",
        "13": "odds",
        "14": "live tracker",
        "16": "basic info",
        "17": "team bage"
    }
    rules = {}
    required_length = 16
    for f in mt:
        if "sportId" in f \
                and f["sportId"] == sport \
                and "tournamentStageId" in f \
                and f["tournamentStageId"] == stage:
            rules.update({feature_names[str(f["featureId"])]: f["providers"][0]["name"]})
    if len(rules) < required_length:
        for f in mt:
            if "sportId" in f \
                    and f["sportId"] == sport\
                    and "tournamentStageId" not in f:
                rules.update({feature_names[str(f["featureId"])]: f["providers"][0]["name"]})
    return rules


print(find_priority_rules(_mt, _sport, _stage))
