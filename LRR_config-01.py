import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('_________',
                         bootstrap_servers=['___________'])

for message in consumer:
    JSONRawDataString = message.value
    JSONData = json.loads(JSONRawDataString)
    if "LRR_config" in JSONData:
        print(JSONData)
