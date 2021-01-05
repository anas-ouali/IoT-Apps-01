import ntplib
from datetime import datetime
from time import ctime

c = ntplib.NTPClient()
response = c.request('europe.pool.ntp.org', version=3)
print("response.tx_time:", response.tx_time)

print("ctime(response.tx_time):", ctime(response.tx_time))
print("datetime.utcfromtimestamp(response.tx_time):", datetime.utcfromtimestamp(response.tx_time).strftime("%Y-%m-%dT%H:%M:%S.%f"))
# CurrentTime = datetime.now()
# print("CurrentTime:", CurrentTime)
# TimeStampSHA = CurrentTime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "+01:00"
# print(TimeStampSHA)