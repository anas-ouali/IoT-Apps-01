import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('_________________________',
                         bootstrap_servers=['___________________'])

for message in consumer:
    JSONRawDataString = message.value
    # print (JSONRawDataString)
    JSONData = json.loads(JSONRawDataString)
    # print(JSONData)
    if "DevEUI_uplink" in JSONData and "payload_hex" in JSONData["DevEUI_uplink"]:
        DevEUI = JSONData["DevEUI_uplink"]["DevEUI"]
        if DevEUI in ["______"]:
            # print("DevEUI:",DevEUI)
            Payload_HEX = JSONData['DevEUI_uplink']['payload_hex']
            Latitude = 90 / 8388608 * int(Payload_HEX[0:6],16)
            # print("Latitude:",Latitude)
            Longitude = 180 / 8388608 * int(Payload_HEX[6:12],16)
            # print("Longitude:",Longitude)
            Altitude = int(Payload_HEX[12:16],16)
            print("Message Topic:", message.topic, message.offset , \
                  "- DevEUI:", DevEUI, "- Latitude:", Latitude, "- Longitude:", Longitude, "- Altitude:",Altitude, \
                  "- Frame Count:", JSONData["DevEUI_uplink"]["FCntDn"])