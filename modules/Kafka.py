import json
from kafka import KafkaProducer, KafkaConsumer

from modules import Log


def produce(environment, topic, key, message):
    bootstrap_servers = ["{}-kafka-0.ls.seo:9092".format(environment), "{}-kafka-1.ls.seo:9092".format(environment)]
    topic = topic
    key = bytes(key + "-collector", 'utf-8')
    message = bytes(json.dumps(message), 'utf-8')

    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    if producer.send(topic, key=key, value=message):
        return "OK", 200
    else:
        return "Something went wrong", 500


def consume(environment, topic):
    bootstrap_servers = ["{}-kafka-0.ls.seo:9092".format(environment), "{}-kafka-1.ls.seo:9092".format(environment)]
    topic = topic
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, auto_offset_reset="earliest")
    for message in consumer:
        message_str = message.value.decode('utf-8')
        return message_str, 200
    Log.warning("No message gotten from '{}' topic ({})".format(topic, environment))
    return "Something went wrong", 500
