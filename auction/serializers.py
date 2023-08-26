from rest_framework import serializers
from .models import CardAuction, CardAuctionBid

class CardAuctionSerializer(serializers.ModelSerializer):
    card_details = serializers.SerializerMethodField()
    class Meta:
        model = CardAuction
        fields = '__all__'
    
    def get_card_details(self, obj):
        return obj.get_card_details

class CreateCardAuctionSerializer(serializers.ModelSerializer):
    card_id = serializers.IntegerField()
    starting_price = serializers.IntegerField()
    duration = serializers.IntegerField()
    class Meta:
        model = CardAuction
        fields = ['card_id', 'starting_price', 'duration']
    
    def validate(self, attrs):
        card_id = attrs.get("card_id", "")
        seller_id = attrs.get("seller_id", "")
        starting_price = attrs.get("starting_price", "")
        duration = attrs.get("duration", "")
        if not card_id:
            raise serializers.ValidationError("Card ID is required")
        if not starting_price:
            raise serializers.ValidationError("Starting price is required")
        if not duration:
            raise serializers.ValidationError("Duration is required")
        return attrs

class CardAuctionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAuctionBid
        fields = '__all__'