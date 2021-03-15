import json
import os
import time

from modules import FileManager, Kafka, Log
from modules.Constants import MODULES_DIR
from modules.PushNotificationTesting.KafkaMessageModel import KafkaMessageModel


class PushRegressionDispatcher(object):
    event_data_model = {}
    test_data = []
    response_data = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PushRegressionDispatcher, cls).__new__(cls)
        return cls.instance

    def clear_test_data_list(self):
        self.test_data = []

    def clear_response_data_list(self):
        self.response_data = []

    def set_test_data_list(self, json_data):
        self.test_data = json_data

    def get_response_data_list(self):
        return self.response_data

    def get_test_data_list(self):
        return self.response_data

    def add_item_to_response_data_list(self, json_data):
        self.response_data.append(json_data)

    def run_regression(self, env, spid, eid):
        Log.warning("Regression run is started")
        KMM = KafkaMessageModel().set_environment(env).set_sport_id(spid).set_event_id(eid).get_event_data()
        json_data = json.loads(
            FileManager.get_file(os.path.join(MODULES_DIR, "PushNotificationTesting"), "TestDataSet.json")[0])
        self.set_test_data_list(json_data)
        for test_item in self.test_data:
            current_payload = KMM.make_test_model(test_item["action"], test_item["extra_data"])
            test_item["timestamp"] = int(time.time())
            test_item["expected_result"]["message"] = test_item["expected_result"]["message"].format(
                TEAM1=current_payload["d"]["T1"][0]["Nm"],
                TEAM2=current_payload["d"]["T2"][0]["Nm"]
            )
            test_item["expected_result"]["title"] = test_item["expected_result"]["title"].format(
                TEAM1=current_payload["d"]["T1"][0]["Nm"],
                TEAM2=current_payload["d"]["T2"][0]["Nm"]
            )
            Kafka.produce(env, "notification_rs", "8-" + eid,
                          KMM.make_test_model(test_item["action"], test_item["extra_data"]))
            time.sleep(1)
        Log.warning("Regression run is finished")
        return ["Regression run is finished", 200]

    def retrieve_push(self, timestamp, app_name, title, descr):
        self.response_data.append({"timestamp": timestamp, "app_name": app_name, "title": title, "descr": descr})

    def save_push_data(self, timestamp, app_name, title, descr):
        with open('night-push.log', 'a') as file:
            file.write(json.dumps({"timestamp": timestamp, "app_name": app_name, "title": title, "descr": descr}) + "\n")

    def get_results(self):
        return {"test_data": self.test_data, "response_data": self.response_data}, 200
