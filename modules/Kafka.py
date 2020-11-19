import json
from kafka import KafkaProducer


def produce(environment, topic, key, message):
    bootstrap_servers = ["{}-kafka-0.ls.seo:9092".format(environment), "{}-kafka-1.ls.seo:9092".format(environment)]
    topic = topic
    key = bytes(key, 'utf-8')
    message = bytes(json.dumps(message), 'utf-8')

    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    if producer.send(topic, key=key, value=message):
        return "OK", 200
    else:
        return "Something went wrong", 500

