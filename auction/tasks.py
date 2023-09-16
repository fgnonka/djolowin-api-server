# tasks.py
from celery import shared_task
from datetime import timedelta
from typing import Optional

from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

from card import tasks as card_tasks
from custom_user import tasks as user_tasks
from notification import tasks as notification_tasks

from . import AuctionEvents
from .models import CardAuction, CardAuctionEvent


@shared_task
def check_auction_end():
    all_auctions = CardAuction.objects.filter(auction_complete=False)
    for auction in all_auctions:
        # If the auction has expired, we need to check if there is a current bid
        if auction.has_expired:
            auction_id = auction.id
            seller_id = auction.seller_id
            current_bid = auction.current_bid
            # We dispatch an event to mark the auction as ended
            card_auction_ended_event.delay(
                seller_id=seller_id,
                auction_id=auction_id,
                payload={
                    "auction_id": auction_id,
                    "seller_id": seller_id,
                },
            )
            # If there is a current bid, we need to transfer the coins to the seller and transfer the card to the highest bidder
            if current_bid > 0:
                highest_bidder = auction.highest_bidder
                auction_details = {
                    "auction_id": auction_id,
                    "seller_id": seller_id,
                    "current_bid": current_bid,
                    "highest_bidder": highest_bidder,
                }
                user_tasks.transfer_coins_to_seller(auction_details)
                card_tasks.transfer_card_ownership.delay(
                    auction.card_id, highest_bidder
                )
                auction.sold = True
                card_auction_sold_event.delay(
                    seller_id=seller_id,
                    winner_id=highest_bidder.id,
                    payload=auction_details,
                )
            else:
                auction.sold = False
            # Regardless of whether there is a current bid, we need to mark the auction as ended in the database
            auction.auction_complete = True
            auction.save()


@shared_task
def check_auction_ending_soon():
    all_auctions = CardAuction.objects.filter(auction_complete=False)
    for auction in all_auctions:
        if auction.is_ending_soon:
            for watcher in auction.watchers.all():
                notification_tasks.send_auction_ending_soon_email.delay(
                    watcher.user_id, **auction.get_card_details
                )


# ---------------------------- AUCTION EVENTS ----------------------------#


@shared_task
def card_auction_created_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_CREATED,
        payload=payload,
    )


@shared_task
def card_auction_ended_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_ENDED,
        payload=payload,
    )


@shared_task
def card_auction_won_event(
    *, seller_id: int, auction_id: int, winner_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        winner_id=winner_id,
        event_type=AuctionEvents.AUCTION_WON,
        payload=payload,
    )


@shared_task
def card_auction_cancelled_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_CANCELLED,
        payload=payload,
    )


@shared_task
def bid_placed_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_BID_PLACED,
        payload=payload,
    )


@shared_task
def bid_rejected_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_BID_REJECTED,
        payload=payload,
    )


@shared_task
def card_auction_reported_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_REPORTED,
        payload=payload,
    )


@shared_task
def card_auction_report_rejected_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_REPORT_REJECTED,
        payload=payload,
    )


@shared_task
def card_auction_followed_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_FOLLOWED,
        payload=payload,
    )


@shared_task
def card_auction_unfollowed_event(
    *, seller_id: int, auction_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        event_type=AuctionEvents.AUCTION_UNFOLLOWED,
        payload=payload,
    )


@shared_task
def card_auction_sold_event(
    *, seller_id: int, auction_id: int, winner_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        winner_id=winner_id,
        event_type=AuctionEvents.AUCTION_SOLD,
        payload=payload,
    )


@shared_task
def card_auction_not_sold_event(
    *, seller_id: int, auction_id: int, winner_id: int, payload: Optional[dict] = None
) -> None:
    CardAuctionEvent.objects.create(
        seller_id=seller_id,
        auction_id=auction_id,
        winner_id=winner_id,
        event_type=AuctionEvents.AUCTION_NOT_SOLD,
        payload=payload,
    )
