from rest_framework import serializers
from .models import PlayerCard

class PlayerCardSerializer(serializers.ModelSerializer):
    player_name = serializers.SerializerMethodField()
    rarity_name = serializers.SerializerMethodField()
    position_name = serializers.SerializerMethodField()
    player_age = serializers.SerializerMethodField()
    jersey_number = serializers.SerializerMethodField()
    total_indexes = serializers.SerializerMethodField()
    nationality = serializers.SerializerMethodField()
    
    class Meta:
        model = PlayerCard
        fields = "__all__"
    
    def get_rarity_name(self, obj):
        return obj.card_rarity_name
    
    def get_player_name(self, obj):
        return obj.get_player_name

    def get_position_name(self, obj):
        return obj.player.position
    
    def get_player_age(self, obj):
        return obj.player.get_player_age
    
    def get_jersey_number(self, obj):
        return obj.player.jersey_number
    
    def get_total_indexes(self, obj):
        return obj.get_total_card_index
    
    def get_nationality(self, obj):
        return obj.player.nationality.name