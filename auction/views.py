from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CardAuction, CardAuctionBid
from .serializers import CardAuctionSerializer, CardAuctionBidSerializer


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
    serializer_class = CardAuctionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)