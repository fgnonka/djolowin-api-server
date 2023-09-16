import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djolowin.settings')
django.setup()


from kafka import KafkaConsumer
from kafka import KafkaProducer


from ... import tasks as notification_tasks

AUCTION_KAFKA_TOPIC = "auction_created"
AUCTION_NOTIFICATION_KAFKA_TOPIC = "auction_notification"
topics = [AUCTION_KAFKA_TOPIC, AUCTION_NOTIFICATION_KAFKA_TOPIC, "test"]

consumer = KafkaConsumer(
    bootstrap_servers="localhost:9092",
)
consumer.subscribe(topics=topics)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
)

print("Starting Auction Notification Consumer from KAFKA...")

while True:
    for message in consumer:
        if message.topic == 'auction_created':
            print("Received in Notification Consumer")
            print(message.topic)
            payload = json.loads(message.value.decode("utf-8"))
            notification_tasks.send_auction_created_email.delay(**payload)
        elif message.topic == 'test':
            print("TESTING")