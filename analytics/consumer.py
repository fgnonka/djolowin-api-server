""""""
import json

from kafka import KafkaConsumer
from kafka import KafkaProducer

AUCTION_KAFKA_TOPIC = "auction_created"
AUCTION_NOTIFICATION_KAFKA_TOPIC = "auction_notification"

consumer = KafkaConsumer(
    AUCTION_NOTIFICATION_KAFKA_TOPIC,
    bootstrap_servers="localhost:9092",
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
)

print("Starting Analytics Consumer from KAFKA...")

while True:
    for message in consumer:
        print("Received from Analytics Consumer")
        auction = json.loads(message.value.decode())
        print(auction)
        