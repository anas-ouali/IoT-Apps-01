import json
from kafka import KafkaConsumer

KafkaINT = '__________'
KafkaEXT = '__________'
KafkaActility = '_____'

consumer = KafkaConsumer('______', bootstrap_servers=[KafkaINT])

for message in consumer:
    JSONRawDataString = message.value
    JSONData = json.loads(JSONRawDataString)
    if "LRR_cnx" in JSONData and "LrcId" in JSONData["LRR_cnx"] \
             and "LrrId" in JSONData["LRR_cnx"] \
             and "Update" in JSONData["LRR_cnx"] \
             and "IpState" in JSONData["LRR_cnx"] \
             and "IecState" in JSONData["LRR_cnx"] \
             and "OpeID" in JSONData["LRR_cnx"] \
             and "npId" in JSONData["LRR_cnx"]:
        # print(message.value)
        print("LRC ID:", JSONData["LRR_cnx"]["LrcId"],
                   "LRR ID:", JSONData["LRR_cnx"]["LrrId"],
                   "Update:", JSONData["LRR_cnx"]["Update"],
                   "IP Status:", JSONData["LRR_cnx"]["IpState"],
                   "IEC Status:", JSONData["LRR_cnx"]["IecState"]
                   )