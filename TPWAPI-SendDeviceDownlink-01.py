import json
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
import requests

TPWUserLogin = "_______________"  # Admin/User Login
TPWUserPassword = "____________"   # Admin/User Password
TPWAPIURL = "__________________"
TPWSubscriberID = "____________"
TPWModuleID = "_________"

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
thingparkID = CredentialsAuthJSONData["thingparkID"]
CredentialsAuthSessionToken = CredentialsAuthJSONData["sessionToken"]  # 1st/Temporary Session Token

# II - Generate an Admin Access Code providing a Supplier ID and a Module ID
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
print(AdminAccessCodeJSONData)
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
print(TPWAPISessionJSONData)
print(SessionToken)
print(SubscriptionHREF)

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
print(RetrieveAllDevicesURL)
print(RetrieveAllDevicesResponse.text)
