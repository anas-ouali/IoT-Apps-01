import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('______________',
                         bootstrap_servers=['______________'])

for message in consumer:
    JSONRawDataString = message.value
    JSONData = json.loads(JSONRawDataString)
    if "LRR_cnx" in JSONData:
        print(JSONData)
