import json
from kafka import KafkaProducer


def produce(topic, key, message):
    bootstrap_servers = ['dev-kafka-0.ls.seo:9092', 'dev-kafka-1.ls.seo:9092']
    topic = topic
    key = bytes(key, 'utf-8')
    message = bytes(json.dumps(message), 'utf-8')

    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer.send(topic, key=key, value=message)

    return "OK", 200
