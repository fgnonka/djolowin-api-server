import json
from kafka import KafkaProducer

from .models import PlayerCard, Bundle

from . import CardEvents

producer = KafkaProducer(bootstrap_servers="localhost:9092")


def obtain_card_payload(card_id):
    card = PlayerCard.objects.get(pk=card_id)
    payload = {
        "card_id": card.id,
        "player_name": card.player.name,
        "rarirty_name": card.rarity.name,
        "owner": card.owner.username if card.owner else None,
        "index": card.index,
        "season": card.season,
        "slug": card.slug,
        "is_locked": card.is_locked,
        "for_sale": card.for_sale,
        "price": card.price,
    }
    return payload


def kafka_card_purchased_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_PURCHASED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_purchase_failed_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_PURCHASE_FAILED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_sold_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_SOLD,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_sale_failed_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_SALE_FAILED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_price_updated_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_PRICE_UPDATED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_marked_for_sale_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_MARKED_FOR_SALE,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_unmarked_for_sale_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_UNMARKED_FOR_SALE,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_locked_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_LOCKED,
        json.dumps(payload).encode("utf-8"),
    )


def kafka_card_unlocked_event(card_id):
    payload = obtain_card_payload(card_id)
    producer.send(
        CardEvents.CARD_UNLOCKED,
        json.dumps(payload).encode("utf-8"),
    )
