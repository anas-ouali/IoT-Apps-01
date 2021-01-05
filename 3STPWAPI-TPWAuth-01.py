import requests
import json

TPWUserLogin = "_______________"  ## Admin Login
TPWUserPassword = "____________"  ## Admin Password
TPWAPIURL = "_______________________"

## I - Authenticate using Admin/User Credentials on ThingPark OS
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
CredentialsAuthSessionToken = CredentialsAuthJSONData["sessionToken"]
## 1st/Temporary Session Token
##
print("thingparkID:", thingparkID)
print("CredentialsAuthSessionToken:", CredentialsAuthSessionToken)
print("CredentialsAuthResponse.cookies:", CredentialsAuthResponse.cookies)
##

## II - Retrieve Vendor /1 "TPW Managed-Activation"
AdminAccessCodeURL = TPWAPIURL + "/thingpark/smp/rest/vendors/1?sessionToken=" + CredentialsAuthSessionToken
AdminAccessCodePayload = ""
AdminAccessCodeHeaders = {
    'Content-Type': "application/json",
    'Accept': "application/json"
}
AdminAccessCodeResponse = requests.request("GET",
                                           AdminAccessCodeURL,
                                           headers=AdminAccessCodeHeaders,
                                           data=AdminAccessCodePayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           )

print(AdminAccessCodeResponse.text)

## II - Retrieve Vendor /4 "Acceptance-Test"
AdminAccessCodeURL = TPWAPIURL + "/thingpark/smp/rest/vendors/4?sessionToken=" + CredentialsAuthSessionToken
AdminAccessCodePayload = ""
AdminAccessCodeHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
AdminAccessCodeResponse = requests.request("GET",
                                           AdminAccessCodeURL,
                                           headers=AdminAccessCodeHeaders,
                                           data=AdminAccessCodePayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           ## Cookies generated after Admin/User Authentication
                                           )
print(AdminAccessCodeResponse.text)

## III - Retrieve Vendor /4 "Acceptance-Test" Subscribers
AdminAccessCodeURL = TPWAPIURL + "/thingpark/smp/rest/vendors/4/subscribers?sessionToken=" + CredentialsAuthSessionToken
AdminAccessCodePayload = ""
AdminAccessCodeHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
AdminAccessCodeResponse = requests.request("GET",
                                           AdminAccessCodeURL,
                                           headers=AdminAccessCodeHeaders,
                                           data=AdminAccessCodePayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           ## Cookies generated after Admin/User Authentication
                                           )
print(AdminAccessCodeResponse.text)
