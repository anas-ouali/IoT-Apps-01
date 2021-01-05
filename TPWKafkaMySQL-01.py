import json
import mysql.connector
from kafka import KafkaConsumer

mydb = mysql.connector.connect(
  host="___________________",
  user="___________",
  passwd="________",
  auth_plugin='mysql_native_password',
  database="_______________")

mycursor = mydb.cursor()

consumer = KafkaConsumer('___________',
                         bootstrap_servers=['_____________________'])

for message in consumer:
    JSONRawDataString = message.value
    JSONData = json.loads(JSONRawDataString)
    if "EUI_uplink" in JSONData and "payload_hex" in JSONData["EUI_uplink"]:
        DevEUI = JSONData["EUI_uplink"]["DevEUI"]
        if DevEUI in ["_________________"]:
            print("DevEUI:",DevEUI)
            Payload_HEX = JSONData['EUI_uplink']['payload_hex']
            Latitude = 90 / 8388608 * int(Payload_HEX[0:6],16)
            print("Latitude:",Latitude)
            Longitude = 180 / 8388608 * int(Payload_HEX[6:12],16)
            print("Longitude:",Longitude)
            Altitude = int(Payload_HEX[12:16],16)
            print("Altitude:",Altitude)
            sql = 'INSERT INTO lora_field_test_data (dev_eui, latitude, longitude, altitude) VALUES (%s, %s, %s, %s)'
            val = (DevEUI, Latitude, Longitude, Altitude)
            mycursor.execute(sql, val)
            mydb.commit()
            print("1 record inserted, ID:", mycursor.lastrowid)
