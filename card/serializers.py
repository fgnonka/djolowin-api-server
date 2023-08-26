from rest_framework import serializers
from .models import PlayerCard

class PlayerCardSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField(read_only=True)
    rarity_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PlayerCard
        fields = "__all__"
    
    def get_rarity_name(self, obj):
        return obj.card_rarity_name