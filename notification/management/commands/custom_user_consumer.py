import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()

from kafka import KafkaConsumer
from kafka import KafkaProducer


from ... import tasks as notification_tasks
from custom_user import list_of_customer_events, CustomerEvents


topics = list_of_customer_events
consumer = KafkaConsumer(
    bootstrap_servers="localhost:9092",
)

consumer.subscribe(topics=topics)

print("Starting User Notification Consumer from KAFKA...")

while True:
    for message in consumer:
        print(message.topic)
        if message.topic == CustomerEvents.ACCOUNT_CREATED:
            print("Account created event received")
            payload = json.loads(message.value.decode("utf-8"))
            notification_tasks.send_verification_email.delay(payload["user_id"])
            notification_tasks.setup_notification_preferences.delay(
                payload["user_id"]
            )

        elif message.topic == CustomerEvents.ACCOUNT_VERIFIED:
            print("Account verified event received")
            payload = json.loads(message.value.decode("utf-8"))
            notification_tasks.send_welcome_email.delay(
                email=payload["email"], username=payload["username"]
            )

        elif message.topic == CustomerEvents.PASSWORD_RESET_REQUEST:
            print("Password reset request event received")
            payload = json.loads(message.value.decode("utf-8"))
            notification_tasks.send_password_reset_email.delay(
                user_id=payload["user_id"]
            )

        elif message.topic == CustomerEvents.PASSWORD_RESET_BY_USER:
            print("Password reset by user event received")
            payload = json.loads(message.value.decode("utf-8"))
            notification_tasks.send_password_change_confirmation_email.delay(
                email=payload["email"], username=payload["username"]
            )
