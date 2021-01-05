import json
import requests

TPWUserLogin = "_____________" # Admin Login
TPWUserPassword = "__________"  # Admin Password
TPWAPIURL = "________________"
TPWSubscriberID = "__________"
TPWModuleID = "______________"

# I - Authenticate using Admin/User Credentials on ThingPark OS
CredentialsAuthURL = TPWAPIURL + "/thingpark/smp/rest/admins/login"
CredentialsAuthPayload = "{\"login\": \"" + TPWUserLogin + "\",\"password\": \"" + TPWUserPassword + "\"}"
CredentialsAuthHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
CredentialsAuthResponse = requests.post(CredentialsAuthURL,
                                           headers=CredentialsAuthHeaders,
                                           data=CredentialsAuthPayload
                                           )

CredentialsAuthJSONData = json.loads(CredentialsAuthResponse.text)
thingparkID = CredentialsAuthJSONData["thingparkID"]
CredentialsAuthSessionToken = CredentialsAuthJSONData["sessionToken"]  # 1st/Temporary Session Token
print(CredentialsAuthResponse.text)
print(thingparkID)
print(CredentialsAuthSessionToken)

# II - Generate an Admin Access Code providing a Supplier ID and a Module ID
AdminAccessCodeURL = TPWAPIURL + "/thingpark/smp/rest/admins/" + thingparkID + \
                     "/accessCode?sessionToken=" + CredentialsAuthSessionToken
AdminAccessCodePayload = "{\"subscriberID\": \"" + TPWSubscriberID + "\", \"moduleID\": \"" + TPWModuleID + "\"}"
AdminAccessCodeHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

AdminAccessCodeResponse = requests.post(AdminAccessCodeURL,
                                           headers=AdminAccessCodeHeaders,
                                           data=AdminAccessCodePayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           # Cookies generated after Admin/User Authentication
                                           )
AdminAccessCodeJSONData = json.loads(AdminAccessCodeResponse.text)
AccessCode = AdminAccessCodeJSONData["accessCode"]  # Session Access Code
print(AccessCode)

# III - Create a session on ThingPark Wireless API
TPWAPISessionURL = TPWAPIURL + "/thingpark/wireless/rest/customers?adminAccessCode=" + \
                   AccessCode + "&type=SUBSCRIBER"  # Type: SUPPLIER / SUBSCRIBER
TPWAPISessionPayload = ""
TPWAPISessionHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json",
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
print(TPWAPISessionResponse.text)
print(TPWAPISessionJSONData)
print(SessionToken)
print(SubscriptionHREF)

# IV - Retrieve Application Servers
RetrieveAppServersURL = TPWAPIURL + "/thingpark/wireless/rest" + SubscriptionHREF + "/appServers?sessionToken=" + SessionToken
RetrieveAppServersPayload = ""
RetrieveAppServersHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}
RetrieveAppServersResponse = requests.get(RetrieveAppServersURL,
                                     headers=RetrieveAppServersHeaders,
                                     data=RetrieveAppServersPayload,
                                     cookies=TPWAPISessionResponse.cookies
                                     # Cookies generated after TPW Session
                                     )

print(RetrieveAppServersResponse.text)
AppServerJSONData = json.loads(RetrieveAppServersResponse.text)

# V - Activate/Deactivate Application Server(s)
for i in range(len(AppServerJSONData['briefs'])):
    print(AppServerJSONData['briefs'][i]['href'])
    DeactivateAppServerURL = TPWAPIURL + AppServerJSONData['briefs'][i]['href'] + "?sessionToken=" + SessionToken
    DeactivateAppServerPayload = "{\"state\": \"ACTIVE\"}" #ACTIVE/DEACTIVATED
    DeactivateAppServerHeaders = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    DeactivateAppServerResponse = requests.put(DeactivateAppServerURL,
                                         headers=DeactivateAppServerHeaders,
                                         data=DeactivateAppServerPayload,
                                         cookies=TPWAPISessionResponse.cookies
                                         # Cookies generated after TPW Session
                                         )
    print("Response:")
    print(DeactivateAppServerResponse.text)