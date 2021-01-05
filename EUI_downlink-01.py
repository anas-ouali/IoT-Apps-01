import json
from kafka import KafkaConsumer

KafkaINT = '___________'
KafkaEXT = '_____________'
KafkaActility = '_________'

consumer = KafkaConsumer('________', bootstrap_servers=[KafkaINT])

for message in consumer:
    JSONRawDataString = message.value
    JSONData = json.loads(JSONRawDataString)
    if "EUI_downlink" in JSONData:
        print(JSONData)