import requests


TPWAPIURL = "_____________________"
DevEUI = "______________"
FPort = "2"
Payload = "_______"

QueryString = "DevEUI=" + DevEUI + "&FPort=" + FPort + "&Payload=" + Payload

SendDownlinkURL = TPWAPIURL + "/thingpark/lrc/rest/downlink?" + QueryString
SendDownlinkHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}
SendDownlinkPayload = ""
SendDownlinkResponse = requests.request("POST",
                                           SendDownlinkURL,
                                           headers=SendDownlinkHeaders,
                                           data=SendDownlinkURL
                                           )
print("#1 - Send Downlink")
print("URL:", SendDownlinkURL)
print("Headers:", SendDownlinkHeaders)
print("Payload:", SendDownlinkPayload)
print("Response:", SendDownlinkResponse)
print("Response Text:", SendDownlinkResponse.text)
print("Cookies:", SendDownlinkResponse.cookies)