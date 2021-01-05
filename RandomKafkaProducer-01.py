from kafka import KafkaProducer
import time
import datetime

# print(bytes(str(1).encode('utf-8')))
WaitTime = 0.0
# producer = KafkaProducer(bootstrap_servers='______________________')
i = 0
for i in range(1000):
    CurrentTime = datetime.datetime.now()
    TimeStamp = CurrentTime.strftime("%Y-%m-%dT%H:%M:%S.%f")
    MessageBody = "Topic1 - Message #" + str(i) + ": " + TimeStamp
    # producer.send('Topic1', bytes(MessageBody.encode("utf-8")))
    print(MessageBody)
    time.sleep(WaitTime)
    CurrentTime = datetime.datetime.now()
    TimeStamp = CurrentTime.strftime("%Y-%m-%dT%H:%M:%S.%f")
    MessageBody = "Topic2 - Message #" + str(i) + ": " + TimeStamp
    # producer.send('Topic2', bytes(MessageBody.encode("utf-8")))
    print(MessageBody)
    time.sleep(WaitTime)
    CurrentTime = datetime.datetime.now()
    TimeStamp = CurrentTime.strftime("%Y-%m-%dT%H:%M:%S.%f")
    MessageBody = "Topic3 - Message #" + str(i) + ": " + TimeStamp
    # producer.send('Topic3', bytes(MessageBody.encode("utf-8")))
    print(MessageBody)
    time.sleep(WaitTime)