import graphene
from graphene_django import DjangoObjectType


from playercard.models import CardRarity, PlayerCard


class PlayerCardNode(DjangoObjectType):
    """DjangoObjectType for PlayerCard"""
    playercard_id = graphene.Int()
    total_card_index = graphene.Int()
    absolute_url = graphene.String()
    class Meta:
        model = PlayerCard
        fields = (
            "card_id",
            "player",
            "rarity",
            "owner",
            "index",
            "number_likes",
            "price",
            "edition",
            "is_public",
            "index",
            "is_locked",
            "date_updated",
            "playercard_id",
            "total_card_index",
            "absolute_url"
        )
        filter_fields = {
            "rarity__name": ["exact", "icontains", "istartswith"],
            "player__name": ["exact", "icontains", "istartswith"],
            "owner__username": ["exact", "icontains", "istartswith"],
            "owner__id": ["exact"],
        }
        interfaces = (graphene.relay.Node,)
        skip_registry = True
    
    def resolve_absolute_url(self, info):
        return self.get_absolute_url()

    def resolve_playercard_id(self, info):
        return self.get_playercard_id()
    
    def resolve_total_card_index(self, info):
        return self.get_total_card_index
    

class CardRarityType(DjangoObjectType):
    """DjangoObjectType for CardRarity"""

    class Meta:
        model = CardRarity
        fields = "__all__"
