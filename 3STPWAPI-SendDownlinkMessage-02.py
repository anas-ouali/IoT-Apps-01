import requests
import hashlib
import datetime

TPWAPIURL = "_______________"
DevEUI = "_______"
FPort = "5"
Payload = "1234"
AS_ID = "______"
LRCASKey = "______"
LRCASKey = LRCASKey.lower()

# I.1 - Calculate Timestamp
CurrentTime = datetime.datetime.now()
print("CurrentTime:", CurrentTime)
TimeStampSHA = CurrentTime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "+01:00"
TimeStampURL = TimeStampSHA.replace(":", "%3A")
TimeStampURL = TimeStampURL.replace("+", "%2B")
print("SHA Time Stamp:", TimeStampSHA)
print("URL Time Stamp:", TimeStampURL)

# I.2 - Calculate Token <QueryParameters><ASKey>
QueryStringSHA = "DevEUI=" + DevEUI + "&FPort=" + FPort + "&Payload=" + Payload + "&AS_ID=" + AS_ID \
                 + "&Time=" + TimeStampSHA
SHA2String = QueryStringSHA + LRCASKey
SHA2Token = hashlib.sha256(SHA2String.encode("utf-8")).hexdigest()
print(hashlib.sha256(LRCASKey.encode("utf-8")).hexdigest())
print("URL String:", QueryStringSHA)
print("SHA String:", SHA2String)
print("Token = ", SHA2Token)

# II - Send Downlink
QueryStringURL = "DevEUI=" + DevEUI + "&FPort=" + FPort + "&Payload=" + Payload + "&AS_ID=" + AS_ID \
                 + "&Time=" + TimeStampURL
SendDownlinkURL = TPWAPIURL + "/thingpark/lrc/rest/downlink?" + QueryStringURL + "&Token=" + SHA2Token
SendDownlinkHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}
SendDownlinkPayload = ""
SendDownlinkResponse = requests.request("POST",
                                           SendDownlinkURL,
                                           headers=SendDownlinkHeaders,
                                           data=SendDownlinkURL
                                           )
print("## Send Downlink")
print("URL:", SendDownlinkURL)
print("Headers:", SendDownlinkHeaders)
print("Payload:", SendDownlinkPayload)
print("Response:", SendDownlinkResponse)
print("Response Text:", SendDownlinkResponse.text)
print("Cookies:", SendDownlinkResponse.cookies)
