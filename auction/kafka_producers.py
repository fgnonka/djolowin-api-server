import json
import time
from kafka import KafkaProducer

from .models import CardAuction
from . import AuctionEvents

AUCTION_KAFKA_TOPIC = "auction_created"
AUCTION_LIMIT = 1000

producer = KafkaProducer(bootstrap_servers="localhost:9092")



def obtain_auction_payload(auction_id):
    auction = CardAuction.objects.get(pk=auction_id)
    card = auction.card
    seller = auction.seller
    starting_price = auction.starting_price
    end_time = auction.end_time
    start_time = auction.start_time
    payload = {
        "auction_id": auction.id,
        "card_details": card.get_card_details,
        "seller_id": seller.id,
        "seller_name": seller.username,
        "starting_price": starting_price,
        "current_bid": auction.current_bid,
        "highest_bidder": auction.highest_bidder.username
        if auction.highest_bidder
        else None,
        "start_time": str(start_time),
        "duration": auction.duration,
        "end_time": str(end_time),
    }
    return payload


def kafka_auction_created_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_CREATED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_ended_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_ENDED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_cancelled_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_CANCELLED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_bid_placed_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_BID_PLACED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_reported_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_REPORTED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_followed_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_FOLLOWED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_unfollowed_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_UNFOLLOWED,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_sold_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_SOLD,
        json.dumps(payload).encode("utf-8"),
    )

def kafka_auction_not_sold_event(auction_id):
    payload = obtain_auction_payload(auction_id)
    producer.send(
        AuctionEvents.AUCTION_NOT_SOLD,
        json.dumps(payload).encode("utf-8"),
    )
