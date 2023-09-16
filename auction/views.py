from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_models.models import PlayerCard, UserWallet
from .models import CardAuction, CardAuctionBid
from .serializers import (
    CardAuctionSerializer,
    CardAuctionBidSerializer,
    CreateCardAuctionSerializer,
    CreateBidSerializer,
)
from .kafka_producers import kafka_auction_created_event
from . import tasks as auction_tasks
from notification import tasks as notification_tasks


class CardAuctionDetailView(generics.RetrieveUpdateAPIView):
    queryset = CardAuction.objects.all()
    serializer_class = CardAuctionSerializer


class ActiveCardAuctionListView(generics.ListAPIView):
    queryset = CardAuction.objects.filter(auction_complete=False).order_by("end_time")
    serializer_class = CardAuctionSerializer
    serializer_class = CardAuctionSerializer


class OwnedCardAuctionListView(APIView):
    serializer_class = CardAuctionSerializer

    def get(self, request, format=None):
        queryset = CardAuction.objects.filter(seller=request.user)
        return Response(self.serializer_class(queryset, many=True).data)


class CardAuctionBidView(generics.RetrieveUpdateAPIView):
    queryset = CardAuctionBid.objects.all()
    serializer_class = CardAuctionBidSerializer


class CreateCardAuctionView(generics.CreateAPIView):
    queryset = CardAuction.objects.all()
    serializer_class = CreateCardAuctionSerializer

    def post(self, request, *args, **kwargs):
        card_id = request.data["data"]["card_id"]
        card = PlayerCard.objects.get(pk=card_id)
        # Check if the card belongs to the user creating the auction
        if card.owner_id != request.user.id:
            return Response(
                {"message": "You do not own this card"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Check if card is already in auction
        try:
            last_auction = CardAuction.objects.filter(card_id=card_id).latest(
                "end_time"
            )
            if last_auction.auction_complete == False:
                return Response(
                    {"message": "Card is already in auction"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CardAuction.DoesNotExist:
            pass
        serializer = CreateCardAuctionSerializer(data=request.data["data"])
        if serializer.is_valid():
            serializer.save(seller_id=request.user.id)
            auction = CardAuctionSerializer(serializer.instance).data
            # Lock the card so it cannot be traded while in auction
            card.is_locked = True
            card.save()
            auction_tasks.card_auction_created_event.delay(
                seller_id=request.user.id,
                auction_id=auction["id"],
                payload={
                    "auction_id": auction["id"],
                    "seller_id": request.user.id,
                    "card_id": card_id,
                },
            )
            kafka_auction_created_event(auction["id"])
            return Response(
                {
                    "message": "Card auction created successfully",
                    "auction": auction,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceBidView(generics.CreateAPIView):
    queryset = CardAuctionBid.objects.all()
    serializer_class = CreateBidSerializer

    def post(self, request, *args, **kwargs):
        auction_id = request.data["auction"]
        auction = CardAuction.objects.get(pk=auction_id)
        # Check if the auction belongs to the user placing the bid
        if auction.seller == request.user:
            return Response(
                {"message": "You cannot bid on your own auction"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Check if the auction has expired
        if auction.has_expired:
            return Response(
                {"message": "Auction has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        submitted_bid = request.data["amount"]
        # Check if the bid is higher than the current bid
        if submitted_bid <= auction.current_bid:
            return Response(
                {"message": "Bid must be higher than current bid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CreateBidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(bidder_id=request.user.id)
            bid = CardAuctionBidSerializer(serializer.instance).data
            if auction.highest_bidder:
                # Notify the previous highest bidder that they have been outbid
                notification_tasks.send_auction_outbid_email.delay(
                    bidder_id=auction.highest_bidder.id,
                    auction=auction,
                    bid_amount=bid["amount"],
                )

                # Refund the previous highest bidder
                refund_wallet = UserWallet.objects.get(user_id=auction.highest_bidder)
                refund_wallet.balance += auction.current_bid
                refund_wallet.reserved_balance -= auction.current_bid
                refund_wallet.save()

            # Update the user's wallet
            wallet = UserWallet.objects.get(user_id=request.user.id)
            wallet.balance -= int(bid["amount"])
            wallet.reserved_balance += int(bid["amount"])
            wallet.save()

            # Update the auction with the new bid and set the highest bidder
            auction.current_bid = int(bid["amount"])
            auction.highest_bidder = request.user.id
            auction.save()
            return Response(
                {
                    "message": "Bid placed successfully",
                    "bid": bid,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BidListView(generics.ListAPIView):
    serializer_class = CardAuctionBidSerializer

    def get(self, request, *args, **kwargs):
        try:
            auction = CardAuction.objects.get(pk=kwargs["pk"])
            queryset = CardAuctionBid.objects.filter(auction=auction)
            return Response(self.serializer_class(queryset, many=True).data)
        except CardAuction.DoesNotExist:
            return Response(
                {"message": "Auction does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
