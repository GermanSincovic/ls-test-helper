from kafka import KafkaConsumer


def consume(environment, topic):
    bootstrap_servers = ["{}-kafka-0.ls.seo:9092".format(environment), "{}-kafka-1.ls.seo:9092".format(environment)]
    topic = topic
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, auto_offset_reset="latest")
    for message in consumer:
        print(message.value)


if __name__ == '__main__':
    consume("dev", "export-mapping-template")
