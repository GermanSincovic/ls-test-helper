# import json
from google.protobuf.json_format import MessageToDict
from kafka import KafkaConsumer
# from google.protobuf.descriptor_pool import DescriptorPool

bootstrap_servers = ["dev-kafka-0.ls.seo:9092", "dev-kafka-1.ls.seo:9092"]
consumer = KafkaConsumer("envelope", bootstrap_servers=bootstrap_servers)

with open("test/base_model.proto", "r") as proto:
    for message in consumer:
        print(MessageToDict(message.value, descriptor_pool=proto))



# pool = DescriptorPool()
# print(pool)
# pool.Add('C:\\Users\\IDidyk\\Desktop\\base_model.proto')

# print(MessageToDict(message))
