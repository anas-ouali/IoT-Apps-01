import json
import requests

TPWUserLogin = "___________________"  # Admin Login
TPWUserPassword = "________________"   # Admin Password
TPWAPIURL = "______________________"
TPWSubscriberID = "_______________"
subscriberUid = TPWSubscriberID[1:]

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

# II - Get Subscriber Users
GetSubscriberURL = TPWAPIURL + "/thingpark/smp/rest/subscribers/" + subscriberUid + "/users?sessionToken=" + CredentialsAuthSessionToken
GetSubscriberPayload = ""
GetSubscriberHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
GetSubscriberResponse = requests.get(GetSubscriberURL,
                                           headers=GetSubscriberHeaders,
                                           data=GetSubscriberPayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           )
print(GetSubscriberResponse.text)
GetSubscriberJSONData = json.loads(GetSubscriberResponse.text)

## III - Lock/Unlock Users

for i in range(len(GetSubscriberJSONData['briefs']['brief'])):
    print(GetSubscriberJSONData['briefs']['brief'][i]['ID'])
    LockUserURL = TPWAPIURL + "/thingpark/smp/rest/users/" + GetSubscriberJSONData['briefs']['brief'][i]['ID'] \
                  + "/unlock?sessionToken=" + CredentialsAuthSessionToken ## lock / unlock
    LockUserPayload = ""
    LockUserHeaders = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    LockUserResponse = requests.put(LockUserURL,
                                    headers=LockUserHeaders,
                                    data=LockUserPayload,
                                    cookies=CredentialsAuthResponse.cookies
                                    )
    print("Response Text:", LockUserResponse.text)
    print("Status Code:", LockUserResponse.status_code)
    print("Headers:", LockUserResponse.headers)
    print("Content:", LockUserResponse.content)
    print("OK:", LockUserResponse.ok)