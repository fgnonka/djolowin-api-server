from rest_framework import serializers
from .models import PlayerCard

class PlayerCardSerializer(serializers.ModelSerializer):
    player_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = PlayerCard
        fields = "__all__"