from rest_framework import serializers

from .models import PlayerCard, CardRarity


class PlayerCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerCard
        fields = [
            "card_id",
            "player",
            "rarity",
            "slug",
            "edition",
            "index",
            "owner",
            "number_likes",
            "get_player_name",
        ]


class CardRaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CardRarity
        fields = "__all__"
