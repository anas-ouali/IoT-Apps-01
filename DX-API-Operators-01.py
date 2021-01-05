import requests
import json

## Authenticate using admin credentials on ThingPark OS
url = "_________________________"
payload = "{\"login\": \"_____________\",\"password\": \"________________\"}"
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
response = requests.request("POST", url, headers = headers, data = payload)
## response = requests.post(url, headers=headers, data = payload)
## print("1st Response:",response.text.encode('utf8'))
JSONData = json.loads(response.text)
thingparkID = JSONData["thingparkID"]
sessionToken = JSONData["sessionToken"]
JSESSIONID = "JSESSIONID=" + response.cookies['JSESSIONID']
print("thingparkID:",thingparkID)
print("sessionToken:",sessionToken)
##print(response.cookies.values)
print("Cookie:",JSESSIONID)
print("\n\n")

##  Generate an Admin access code providing a supplier or subscriber ID and TPW_NP as module ID
url = "________________________" + thingparkID + "/accessCode?sessionToken=" + sessionToken
payload = "{\"operatorID\": \"_________\", \"moduleID\": \"__________\"}"
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Cookie': JSESSIONID
}
response = requests.request("POST", url, headers = headers, data = payload)
print(response.text.encode('utf8'))
JSONData = json.loads(response.text)
accessCode = JSONData["accessCode"]
print("accessCode:",accessCode)
BearerAccessCode = "Bearer " + accessCode

## Create a session on ThingPark Wireless Networks API
url = "____________________" + accessCode
payload = ""
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
response = requests.get(url, headers = headers)
print("\n\nThingPark Wireless Operators API Session: ",response.text.encode('utf8'))
