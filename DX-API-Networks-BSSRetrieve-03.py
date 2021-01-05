import json
import requests
from datetime import datetime

TPWUserLogin = "_____________"  # Admin/User Login
TPWUserPassword = "_____________"   # Admin/User Password
TPWAPIURL = "_______________"
TPWSupplierID = "________"
TPWModuleID = "___________"

# I - Authenticate using Admin/User Credentials on ThingPark OS
CredentialsAuthURL = TPWAPIURL + "/thingpark/smp/rest/admins/login"
CredentialsAuthPayload = "{\"login\": \"" + TPWUserLogin + "\",\"password\": \"" + TPWUserPassword + "\"}"
CredentialsAuthHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
CredentialsAuthResponse = requests.request("POST",
                                           CredentialsAuthURL,
                                           headers=CredentialsAuthHeaders,
                                           data=CredentialsAuthPayload
                                           )
# print(CredentialsAuthResponse.text)
CredentialsAuthJSONData = json.loads(CredentialsAuthResponse.text)
thingparkID = CredentialsAuthJSONData["thingparkID"]
CredentialsAuthSessionToken = CredentialsAuthJSONData["sessionToken"]  # 1st/Temporary Session Token

# II - Generate an Admin Access Code providing a Supplier ID and a Module ID
AdminAccessCodeURL = TPWAPIURL + "/thingpark/smp/rest/admins/" + thingparkID + \
                     "/accessCode?sessionToken=" + CredentialsAuthSessionToken
AdminAccessCodePayload = "{\"supplierID\": \"" + TPWSupplierID + "\", \"moduleID\": \"" + TPWModuleID + "\"}"
AdminAccessCodeHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

AdminAccessCodeResponse = requests.request("POST",
                                           AdminAccessCodeURL,
                                           headers=AdminAccessCodeHeaders,
                                           data=AdminAccessCodePayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           # Cookies generated after Admin/User Authentication
                                           )
AdminAccessCodeJSONData = json.loads(AdminAccessCodeResponse.text)
AccessCode = AdminAccessCodeJSONData["accessCode"]  # Session Access Code

# III - Create a session on ThingPark Wireless API
TPWAPISessionURL = TPWAPIURL + "/thingpark/wireless/rest/partners?adminAccessCode=" + \
                   AccessCode + "&type=SUPPLIER"  # Type: SUPPLIER / SUBSCRIBER
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
PartnerHREF = TPWAPISessionJSONData["partner"]["href"]  # Partner HREF

# IV - TPWAction / Retrieve All BSS
TPWActionURL = TPWAPIURL + "/thingpark/wireless/rest" + PartnerHREF + "/bss?sessionToken=" + SessionToken
TPWActionPayload = ""
TPWActionHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
TPWActionResponse = requests.get(TPWActionURL,
                                 headers=TPWActionHeaders,
                                 data=TPWActionPayload,
                                 cookies=TPWAPISessionResponse.cookies
                                 # Cookies generated after TPW API Session Creation
                                 )
print(TPWActionResponse.text)
BSSJSONData = json.loads(TPWActionResponse.text)
print(BSSJSONData)


GWIDX = 1
FaultyBSSList = ""

# for i in range(len(BSSJSONData['briefs'])):
#     if BSSJSONData['briefs'][i]['healthState'] == "BACKHAUL_CNX_ERROR":
for i in range(len(BSSJSONData['briefs'])):
    if BSSJSONData['briefs'][i]['healthState'] == "BACKHAUL_CNX_ERROR":
        # TPWRetrieveBSS / Retrieve BSS Details
        TPWRetrieveBSSURL = TPWAPIURL + BSSJSONData['briefs'][i]["href"] + "?sessionToken=" + SessionToken
        TPWRetrieveBSSPayload = ""
        TPWRetrieveBSSHeaders = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        TPWRetrieveBSSResponse = requests.get(TPWRetrieveBSSURL,
                                              headers=TPWRetrieveBSSHeaders,
                                              data=TPWRetrieveBSSPayload,
                                              cookies=TPWAPISessionResponse.cookies
                                              # Cookies generated after TPW API Session Creation
                                              )
        RetrieveBSSJSONData = json.loads(TPWRetrieveBSSResponse.text)
        # print(RetrieveBSSJSONData)
        FaultyBSSList = FaultyBSSList + str(GWIDX) + " " + BSSJSONData['briefs'][i]['name'] + " " \
                        + BSSJSONData['briefs'][i]['lrrID'] + " " \
                        + str(BSSJSONData['briefs'][i]['lat']) + " " \
                        + str(BSSJSONData['briefs'][i]['lon']) + " " \
                        + str(RetrieveBSSJSONData['ints']['int'][0]['ip']) + " " \
                        + str(RetrieveBSSJSONData['ints']['int'][1]['ip']) + " " \
                        + str(datetime.utcfromtimestamp(float(str(RetrieveBSSJSONData['cnxStateSince']))/1000)) + "\n"
        GWIDX = GWIDX + 1
# HTTPDoc = HTTPDoc + "</table></body></html>"
print(FaultyBSSList)
