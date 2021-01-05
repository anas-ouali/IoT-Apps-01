# import smtplib
# from socket import gaierror
#
# # now you can play with your code. Let’s define the SMTP server separately here:
# port = 25
# smtp_server = "_________________"
# login = "__________"
# password = "____________"
#
# # specify the sender’s and receiver’s email addresses
# sender = "_____________"
# receiver = "_______________"
#
# # type your message: use two newlines (\n) to separate the subject from the message body, and use 'f' to
# # automatically insert variables in the text
# message = f"""\
# Subject: Hi Anas,
# To: {receiver}
# From: {sender}
#
# This is my first message with Python."""
#
# try:
#     #send your message with credentials specified above
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.login(login, password)
#         server.sendmail(sender, receiver, message)
#
#     # tell the script to report if your message was sent or which errors need to be fixed
#     print('Sent')
# except (gaierror, ConnectionRefusedError):
#     print('Failed to connect to the server. Bad connection settings?')
# except smtplib.SMTPServerDisconnected:
#     print('Failed to connect to the server. Wrong user/password?')
# except smtplib.SMTPException as e:
#     print('SMTP error occurred: ' + str(e))



from datetime import datetime

timestamp = 1545730073
dt_object = datetime.fromtimestamp(timestamp)

print("dt_object =", dt_object)
print("type(dt_object) =", type(dt_object))