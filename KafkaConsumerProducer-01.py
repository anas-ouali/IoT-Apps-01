from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError

consumer = KafkaConsumer('InputTopic',
                         bootstrap_servers=['localhost:9092'])

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


for message in consumer:
    producer.send('OutputTopic', message.value)
