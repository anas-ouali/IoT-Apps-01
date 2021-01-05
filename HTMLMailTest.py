# import the necessary components first
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
port = 25
smtp_server = "___________"
login = "__________"
password = "_________"
sender_email = "__________"
receiver_email = "_____________"
message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email
# write the plain text part
text = """\
"""
# write the HTML part
html = """\
<html>
  <body>
    <p>Hi,<br>
       Check out the new post on the Mailtrap blog:</p>
    <p><a href="https://blog.mailtrap.io/2018/09/27/cloud-or-local-smtp-server">SMTP Server for Testing: Cloud-based or Local?</a></p>
    <p> Feel free to <strong>let us</strong> know what content would be useful for you!</p>
  </body>
</html>
"""
# convert both parts to MIMEText objects and add them to the MIMEMultipart message
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)
# send your email
with smtplib.SMTP("______________", 25) as server:
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print('Sent')