from datetime import datetime
import requests
from modules import Log


class KafkaMessageModel(object):
    sport_mapping = {
        "1": "soccer",
        "23": "basketball",
        "2": "tennis",
        "5": "ice_hockey",
        "73": "cricket"
    }
    SOURCE_LINK = "https://livescore-{}-api.ls-g.net/scores/{}/~~id/8-{}?tz=3&tzout=3"
    EVENT_DATA = None
    ENVIRONMENT = None
    EVENT_ID = None
    SPORT_ID = None
    BASE_MODEL = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(KafkaMessageModel, cls).__new__(cls)

        return cls.instance

    def set_environment(self, environment):
        self.ENVIRONMENT = environment
        return self

    def set_sport_id(self, sport_id):
        self.SPORT_ID = self.sport_mapping[sport_id]
        return self

    def set_event_id(self, event_id):
        self.EVENT_ID = event_id
        return self

    def get_current_ls_time(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def get_event_data(self):
        if not self.ENVIRONMENT:
            Log.warning("Environment is not set")
        elif not self.SPORT_ID:
            Log.warning("Sport ID is not set")
        elif not self.EVENT_ID:
            Log.warning("Event ID is not set")
        else:
            self.EVENT_DATA = requests.get(
                self.SOURCE_LINK.format(self.ENVIRONMENT, self.SPORT_ID, self.EVENT_ID)).json()
        return self

    def make_base_model(self):
        if not self.EVENT_DATA:
            Log.warning("EVENT_DATA is not set")
        else:
            self.BASE_MODEL = {
                "Spid": self.EVENT_DATA["Spid"],
                "Pid": self.EVENT_DATA["Pid"],
                "Sid": str(self.EVENT_DATA["Stg"]["Sid"]),
                "Eid": str(self.EVENT_DATA["Eid"]),
                "Esd": self.EVENT_DATA["Esd"],
                "T1": [],
                "T2": []
            }
        for T in self.EVENT_DATA["T1"]:
            self.BASE_MODEL["T1"].append({"ID": T["ID"], "Nm": T["Nm"]})
        for T in self.EVENT_DATA["T2"]:
            self.BASE_MODEL["T2"].append({"ID": T["ID"], "Nm": T["Nm"]})
        return self

    def make_test_model(self, action, extra_data):
        self.make_base_model()
        test_model = {"ct": self.get_current_ls_time(), "ac": action, "d": self.BASE_MODEL, "op": 0}
        test_model["d"].update(extra_data)
        return test_model
