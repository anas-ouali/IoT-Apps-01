import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from datetime import datetime


TPWUserLogin = "______________"  ## Admin/User Login
TPWUserPassword = "______________"  ## Admin/User Password
receiver_email = "________________" ## User Email Address
TPWAPIURL = "___________________"
TPWSupplierID = "__________"
TPWModuleID = "____________"


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
CredentialsAuthSessionToken = CredentialsAuthJSONData["sessionToken"]  ## 1st/Temporary Session Token

## II - Generate an Admin Access Code providing a Supplier ID and a Module ID
AdminAccessCodeURL = TPWAPIURL + "/thingpark/smp/rest/admins/" + thingparkID + "/accessCode?sessionToken=" + CredentialsAuthSessionToken
AdminAccessCodePayload = "{\"supplierID\": \"" + TPWSupplierID + "\", \"moduleID\": \"" + TPWModuleID + "\"}"
AdminAccessCodeHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
AdminAccessCodeResponse = requests.request("POST",
                                           AdminAccessCodeURL,
                                           headers=AdminAccessCodeHeaders,
                                           data=AdminAccessCodePayload,
                                           cookies=CredentialsAuthResponse.cookies
                                           ## Cookies generated after Admin/User Authentication
                                           )
AdminAccessCodeJSONData = json.loads(AdminAccessCodeResponse.text)
AccessCode = AdminAccessCodeJSONData["accessCode"]  ## Session Access Code

## III - Create a session on ThingPark Wireless API
TPWAPISessionURL = TPWAPIURL + "/thingpark/wireless/rest/partners?adminAccessCode=" + AccessCode + "&type=SUPPLIER"  ## Type: SUPPLIER / SUBSCRIBER
TPWAPISessionPayload = ""
TPWAPISessionHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
TPWAPISessionResponse = requests.get(TPWAPISessionURL,
                                     headers=TPWAPISessionHeaders,
                                     data=TPWAPISessionPayload,
                                     cookies=AdminAccessCodeResponse.cookies
                                     ## Cookies generated after Access Code Generation
                                     )
TPWAPISessionJSONData = json.loads(TPWAPISessionResponse.text)
SessionToken = TPWAPISessionJSONData["sessionToken"]  ## Definitive Session Token
PartnerHREF = TPWAPISessionJSONData["partner"]["href"]  ## Partner HREF

## IV - TPWAction / Retrieve BSS
TPWActionURL = TPWAPIURL + "/thingpark/wireless/rest" + PartnerHREF + "/bss?sessionToken=" + SessionToken
TPWActionPayload = ""
TPWActionHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
TPWActionResponse = requests.get(TPWActionURL,
                                 headers=TPWActionHeaders,
                                 data=TPWActionPayload,
                                 cookies=TPWAPISessionResponse.cookies
                                 ## Cookies generated after TPW API Session Creation
                                 )
BSSJSONData = json.loads(TPWActionResponse.text)
GWIDX = 1
MailText = "Ci-après la liste des GWs en panne :<br>\
        <style type=\"text/css\">.tg  {border-collapse:collapse;border-spacing:0;}.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;  overflow:hidden;padding:10px 5px;word-break:normal;}.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}</style>\
		<table class=\"tg\">\
			<thead>\
				<tr>\
					<th class=\"tg-0pky\"/>No</th>\
					<th class=\"tg-0pky\"/>Site Name</th>\
					<th class=\"tg-0pky\"/>LRR ID</th>\
					<th class=\"tg-0pky\"/>Latitude</th>\
					<th class=\"tg-0pky\"/>Logitude</th>\
					<th class=\"tg-0pky\"/>Ethernet IP</th>\
					<th class=\"tg-0pky\"/>PPP IP</th>\
                    <th class=\"tg-0pky\"/>Date/Time</th>\
                </tr>\
			</thead>"


for i in range(len(BSSJSONData['briefs'])):
    if BSSJSONData['briefs'][i]['healthState']=="BACKHAUL_CNX_ERROR":

        ## TPWRetrieveBSS / Retrieve BSS Details
        TPWRetrieveBSSURL = TPWAPIURL + BSSJSONData['briefs'][i]["href"] + "?sessionToken=" + SessionToken
        TPWRetrieveBSSPayload = ""
        TPWRetrieveBSSHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        TPWRetrieveBSSResponse = requests.get(TPWRetrieveBSSURL,
                                              headers=TPWRetrieveBSSHeaders,
                                              data=TPWRetrieveBSSPayload,
                                              cookies=TPWAPISessionResponse.cookies
                                              ## Cookies generated after TPW API Session Creation
                                              )
        RetrieveBSSJSONData = json.loads(TPWRetrieveBSSResponse.text)

        MailText = MailText + "<tr>" + "<td class=\"tg-0pky\">" + str(GWIDX) + "</td>" \
                  + "<td class=\"tg-0pky\">" + BSSJSONData['briefs'][i]['name'] + "</td>" \
                  + "<td class=\"tg-0pky\">" + BSSJSONData['briefs'][i]['lrrID'] + "</td>" \
                  + "<td class=\"tg-0pky\">" + str(BSSJSONData['briefs'][i]['lat']) + "</td>" \
                  + "<td class=\"tg-0pky\">" + str(BSSJSONData['briefs'][i]['lon']) + "</td>" \
                  + "<td class=\"tg-0pky\">" + str(RetrieveBSSJSONData['ints']['int'][0]['ip']) + "</td>" \
                  + "<td class=\"tg-0pky\">" + str(RetrieveBSSJSONData['ints']['int'][1]['ip']) + "</td>" \
                  + "<td class=\"tg-0pky\">" + str(
            datetime.utcfromtimestamp(float(str(RetrieveBSSJSONData['cnxStateSince'])) / 1000)) + "</td></tr>\n"

        # MailText = MailText + str(GWIDX) + " "\
        #                + BSSJSONData['briefs'][i]['name'] + " "\
        #                + BSSJSONData['briefs'][i]['lrrID'] + " "\
        #                + str(BSSJSONData['briefs'][i]['lat']) + " "\
        #                + str(BSSJSONData['briefs'][i]['lon']) + "<br>"
        GWIDX = GWIDX + 1
print(MailText)


port = 25
smtp_server = "_____________"
login = "_________"
password = "__________"
sender_email = "____________"
message = MIMEMultipart("alternative")
message["Subject"] = "__________________"
message["From"] = sender_email
message["To"] = receiver_email
# write the plain text part
text = f"""\
{MailText}
"""
# write the HTML part
html = f"""\
<html>
  <body>
    <p>Bonjour,<br><br>
       {MailText}</p>
  </body>
</html>
"""
# convert both parts to MIMEText objects and add them to the MIMEMultipart message
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)
# send your email
with smtplib.SMTP("smtp.gnet.tn", 25) as server:
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print('Sent')