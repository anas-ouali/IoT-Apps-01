## TPWBSSRetrieve Function:
##  - Input:
##          TPWUserLogin        :   Admin/User Login
##          TPWUserPassword     :   Admin/User Login
##          TPWAPIURL           :   TPW API Root URL
##          TPWSupplierID       :   Supplier ID
##          TPWModuleID         :   Module ID
##
##  - Output:
##          JSON Code
##
## Documentation:
##          https://oss-api.thingpark.com/5.2.2/Thingpark-Wireless/network-manager/

import requests
import json


def TPWBSSRetrieve (TPWUserLogin,
                    TPWUserPassword,
                    TPWAPIURL,
                    TPWSupplierID,
                    TPWModuleID):

    ## I - Authenticate using admin credentials on ThingPark OS
    url1 = TPWAPIURL + "/thingpark/smp/rest/admins/login"
    payload1 = "{\"login\": \"" + TPWUserLogin + "\",\"password\": \"" + TPWUserPassword + "\"}"
    headers1 = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    response1 = requests.request("POST", url1, headers = headers1, data = payload1)
    JSONData = json.loads(response1.text)
    thingparkID = JSONData["thingparkID"]
    sessionToken1 = JSONData["sessionToken"]

    ## II - Generate an Admin access code providing a supplier ID and a module ID
    url2 = TPWAPIURL + "/thingpark/smp/rest/admins/" + thingparkID + "/accessCode?sessionToken=" + sessionToken1
    payload2 = "{\"supplierID\": \"" + TPWSupplierID + "\", \"moduleID\": \"" + TPWModuleID + "\"}"
    headers2 = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
    response2 = requests.request("POST", url2, headers = headers2, data = payload2, cookies = response1.cookies)
    JSONData = json.loads(response2.text)
    accessCode = JSONData["accessCode"]

    ## III - Create a session on ThingPark Wireless Networks API
    url3 = TPWAPIURL + "/thingpark/wireless/rest/partners?adminAccessCode=" + accessCode + "&type=SUPPLIER"
    payload3 = ""
    headers3 = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    }
    response3 = requests.get(url3, headers = headers3, data = payload3, cookies = response2.cookies)
    JSONData = json.loads(response3.text)
    sessionToken2 = JSONData["sessionToken"]
    partner_href = JSONData["partner"]["href"]

    ## IV - Retrieve BSS
    url4 = TPWAPIURL + "/thingpark/wireless/rest" + partner_href + "/bss?sessionToken=" + sessionToken2
    payload4 = ""
    headers4 = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    response4 = requests.get(url4, headers = headers4, data = payload4, cookies = response3.cookies)
    return response4.text

TPWUserLogin = "__________________"
TPWUserPassword = "__________________"
TPWAPIURL = "________________"
TPWSupplierID = "________"
TPWModuleID = "____________"

print (TPWBSSRetrieve (TPWUserLogin,
                    TPWUserPassword,
                    TPWAPIURL,
                    TPWSupplierID,
                    TPWModuleID))
