# TPWBSSRetrieve Function:
#  - Input:
#          TPWUserLogin        :   Admin/User Login
#          TPWUserPassword     :   Admin/User Password
#          TPWAPIURL           :   TPW API Root URL
#          TPWSubscriberID     :   Subscriber ID
#          TPWModuleID         :   Module ID
#          TargetDeviceHREF    :   Target Device HREF
#
#  - Output:
#          Byte Stream TPWActionResponse.text.encode("utf8")
#          JSON Object json.loads(TPWActionResponse.text)
#
#
# Documentation:
#          https://oss-api.thingpark.com/5.2.2/Thingpark-Wireless/device-manager/

import json
import requests

TPWUserLogin = "____________________"  # Admin Login
TPWUserPassword = "_________________"  # Admin Password
TPWAPIURL = "_______________________"  # Base URL
TPWSubscriberID = "_________________"  # Subscriber ID
TPWModuleID = "_____________________"  # Module ID

# I - Authenticate using Admin/User Credentials on ThingPark OS
CredentialsAuthURL = TPWAPIURL + "/thingpark/smp/rest/admins/login"
CredentialsAuthPayload = "{\"login\": \"" + TPWUserLogin + "\",\"password\": \"" + TPWUserPassword + "\"}"
CredentialsAuthHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
CredentialsAuthResponse = requests.request("POST",
                                           CredentialsAuthURL,
                                           headers=CredentialsAuthHeaders,
                                           data=CredentialsAuthPayload
                                           )
CredentialsAuthJSONData = json.loads(CredentialsAuthResponse.text)
print("#1 - Authenticate using Admin/User Credentials on ThingPark OS")
print("URL:", CredentialsAuthURL)
print("Payload:", CredentialsAuthPayload)
print("Response:", CredentialsAuthResponse)
print("Response Text:", CredentialsAuthResponse.text)
print("Cookies:", CredentialsAuthResponse.cookies)
thingparkID = CredentialsAuthJSONData["thingparkID"]
CredentialsAuthSessionToken = CredentialsAuthJSONData["sessionToken"]  # 1st/Temporary Session Token

# II - Generate an Admin Access Code providing a Subscriber ID and a Module ID
AdminAccessCodeURL = TPWAPIURL + "/thingpark/smp/rest/admins/" + thingparkID + \
                     "/accessCode?sessionToken=" + CredentialsAuthSessionToken
AdminAccessCodePayload = "{\"subscriberID\": \"" + TPWSubscriberID + "\", \"moduleID\": \"" + TPWModuleID + "\"}"
AdminAccessCodeHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

AdminAccessCodeResponse = requests.request("POST",
                                           AdminAccessCodeURL,
                                           headers=AdminAccessCodeHeaders,
                                           data=AdminAccessCodePayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           # Cookies generated after Admin/User Authentication
                                           )
AdminAccessCodeJSONData = json.loads(AdminAccessCodeResponse.text)
print("\n#2 - Generate an Admin Access Code providing a Subscriber ID and a Module ID")
print("URL:", AdminAccessCodeURL)
print("Payload:", AdminAccessCodePayload)
print("Response:", AdminAccessCodeResponse)
print("Response Text:", AdminAccessCodeResponse.text)
print("Cookies:", AdminAccessCodeResponse.cookies)
AccessCode = AdminAccessCodeJSONData["accessCode"]  # Session Access Code

# III - Create a session on ThingPark Wireless Devices API
TPWAPISessionURL = TPWAPIURL + "/thingpark/wireless/rest/customers?adminAccessCode=" + \
                   AccessCode + "&type=SUBSCRIBER"  # Type: SUPPLIER / SUBSCRIBER
TPWAPISessionPayload = ""
TPWAPISessionHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
TPWAPISessionResponse = requests.get(TPWAPISessionURL,
                                     headers=TPWAPISessionHeaders,
                                     data=TPWAPISessionPayload,
                                     cookies=AdminAccessCodeResponse.cookies
                                     # Cookies generated after Access Code Generation
                                     )
TPWAPISessionJSONData = json.loads(TPWAPISessionResponse.text)
SessionToken = TPWAPISessionJSONData["sessionToken"]  # Definitive Session Token
SubscriptionHREF = TPWAPISessionJSONData["subscription"]["href"]  # Subscription HREF
print("\n#3 - Create a session on ThingPark Wireless Devices API")
print("URL:", TPWAPISessionURL)
print("Payload:", TPWAPISessionPayload)
print("Response:", TPWAPISessionResponse)
print("Response Text:", TPWAPISessionResponse.text)
print("Cookies:", TPWAPISessionResponse.cookies)
# print(SessionToken)
# print(SubscriptionHREF)

# IV - Retrieve All Devices
RetrieveAllDevicesURL = TPWAPIURL + "/thingpark/wireless/rest" + SubscriptionHREF \
                        + "/devices?sessionToken=" + SessionToken
RetrieveAllDevicesPayload = ""
RetrieveAllDevicesHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
RetrieveAllDevicesResponse = requests.get(RetrieveAllDevicesURL,
                                     headers=RetrieveAllDevicesHeaders,
                                     data=RetrieveAllDevicesPayload,
                                     cookies=TPWAPISessionResponse.cookies
                                     # Cookies generated after Access Code Generation
                                     )
RetrieveAllDevicesJSONData = json.loads(RetrieveAllDevicesResponse.text)
# print(RetrieveAllDevicesURL)
# print(RetrieveAllDevicesResponse.text)

# V - Identify Target Device: EUI => Device HREF

Found = False
i = 0
while not Found :
    if RetrieveAllDevicesJSONData["briefs"][i]["EUI"] == "________" :
        TargetDeviceHREF = RetrieveAllDevicesJSONData["briefs"][i]["href"]
        Found = True
    i = i + 1
# print (TargetDeviceHREF)


# VI - Send Downlink Message

SendDownLinkMessageURL = TPWAPIURL + TargetDeviceHREF + "/admins/downlink?payload=_____&fPort=2&sessionToken=" + SessionToken
SendDownLinkMessagePayload = ""
SendDownLinkMessageHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
SendDownLinkMessageResponse = requests.post(SendDownLinkMessageURL,
                                     headers=SendDownLinkMessageHeaders,
                                     data=SendDownLinkMessagePayload,
                                     cookies=TPWAPISessionResponse.cookies
                                     # Cookies generated after Access Code Generation
                                     )
print("\n#4 - Send Downlink Message")
print("URL:", SendDownLinkMessageURL)
print("Response:", SendDownLinkMessageResponse)
print("Response Text:", SendDownLinkMessageResponse.text)
# print(SendDownLinkMessagePayload)