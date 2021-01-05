import requests
import json

## Authenticate using admin credentials on ThingPark OS
url = "____________________________________"
payload = "{\"login\": \"_________________\",\"password\": \"__________________\"}"
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
response = requests.request("POST", url, headers = headers, data = payload)
## response = requests.post(url, headers=headers, data = payload)
## print("1st Response:",response.text.encode('utf8'))

JSONData = json.loads(response.text)

print(JSONData)

thingparkID = JSONData["thingparkID"]
sessionToken = JSONData["sessionToken"]
JSESSIONID = "JSESSIONID=" + response.cookies['JSESSIONID']
print("thingparkID:",thingparkID)
print("sessionToken:",sessionToken)
##print(response.cookies.values)
print("Cookie:",JSESSIONID)
print("\n\n")

##  Generate an Admin access code providing a supplier or subscriber ID and ________________ as module ID
url = "___________________________" + thingparkID + "/accessCode?sessionToken=" + sessionToken
payload = "{\"subscriberID\": \"_______________\", \"moduleID\": \"________________\"}"
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
url = "________________________=" + accessCode
payload = ""
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
response = requests.get(url, headers = headers)
print("\n\nThingPark Subscribers API Session: ",response.text.encode('utf8'))
