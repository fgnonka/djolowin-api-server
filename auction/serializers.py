from rest_framework import serializers
from .models import CardAuction, CardAuctionBid

class CardAuctionSerializer(serializers.ModelSerializer):
    seller_id = serializers.SerializerMethodField()
    card_details = serializers.SerializerMethodField()
    auction_details = serializers.SerializerMethodField()
    class Meta:
        model = CardAuction
        fields = '__all__'
    
    def get_card_details(self, obj):
        return obj.get_card_details
    
    def get_auction_details(self, obj):
        return obj.get_auction_details
    
    def get_seller_id(self, obj):
        return obj.seller.id

class CreateCardAuctionSerializer(serializers.ModelSerializer):
    card_id = serializers.IntegerField()
    starting_price = serializers.IntegerField()
    duration = serializers.IntegerField()
    class Meta:
        model = CardAuction
        fields = ['card_id', 'starting_price', 'duration']
    
    def validate(self, attrs):
        card_id = attrs.get("card_id", "")
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

class CreateBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAuctionBid
        fields = ['auction', 'amount']
    
    def validate(self, attrs):
        auction_id = attrs.get("auction", "")
        bid_amount = attrs.get("amount", "")
        if not auction_id:
            raise serializers.ValidationError("Auction ID is required")
        if not bid_amount:
            raise serializers.ValidationError("Bid amount is required")
        return attrs