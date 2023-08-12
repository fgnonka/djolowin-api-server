from rest_framework import serializers
from .models import CardAuction, CardAuctionBid

class CardAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAuction
        fields = '__all__'

class CardAuctionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAuctionBid
        fields = '__all__'