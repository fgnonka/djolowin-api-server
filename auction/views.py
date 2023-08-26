from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_models.models import PlayerCard
from .models import CardAuction, CardAuctionBid
from .serializers import (
    CardAuctionSerializer,
    CardAuctionBidSerializer,
    CreateCardAuctionSerializer,
)


class CardAuctionDetailView(generics.RetrieveUpdateAPIView):
    queryset = CardAuction.objects.all()
    serializer_class = CardAuctionSerializer


class ActiveCardAuctionListView(generics.ListAPIView):
    queryset = CardAuction.objects.filter(
        Q(start_time__lte=timezone.now()) & Q(end_time__gte=timezone.now())
    ).order_by("end_time")
    serializer_class = CardAuctionSerializer


class OwnedCardAuctionListView(APIView):
    serializer_class = CardAuctionSerializer

    def get(self, request, format=None):
        queryset = CardAuction.objects.filter(seller_id=request.user.id)
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
            if last_auction and last_auction.end_time > timezone.now():
                return Response(
                    {"message": "Card auction already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CardAuction.DoesNotExist:
            pass
        serializer = CreateCardAuctionSerializer(
            data=request.data["data"]
        )
        if serializer.is_valid():
            serializer.save(seller_id=request.user.id)
            auction = CardAuctionSerializer(serializer.instance).data
            # Lock the card so it cannot be traded while in auction
            card.is_locked = True
            return Response(
                {
                    "message": "Card auction created successfully",
                    "auction": auction,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
