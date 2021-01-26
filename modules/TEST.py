import json

from kafka import KafkaConsumer


def consume(environment, topic):
    bootstrap_servers = ["{}-kafka-0.ls.seo:9092".format(environment), "{}-kafka-1.ls.seo:9092".format(environment)]
    topic = topic
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, auto_offset_reset="earliest")
    for message in consumer:
        message_str = message.value.decode('utf-8')
        message_json = json.loads(message_str)
        print(message_json)


if __name__ == '__main__':
    consume("dev", "export-mapping-template")
