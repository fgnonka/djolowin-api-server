import graphene
from graphene_django.filter import DjangoFilterConnectionField


from bundle.models import Bundle
from playercard.models import CardRarity, PlayerCard
from .types import PlayerCardNode, CardRarityType

playercards_queryset = PlayerCard.objects.filter(
    index__gt=0, for_sale=True, is_locked=False, is_public=True
).exclude(bundle__in=Bundle.objects.all())


class PlayerCardQueries(graphene.ObjectType):
    playercard = graphene.relay.node.Field(
        PlayerCardNode, id=graphene.Int(required=True)
    )
    all_playercards = DjangoFilterConnectionField(
        PlayerCardNode, first=graphene.Int(), skip=graphene.Int()
    )
    all_playercards_of_a_cardrarity = graphene.List(
        PlayerCardNode, cardrarity_id=graphene.Int(required=True)
    )
    all_playercards_of_a_player = graphene.List(
        PlayerCardNode, player_id=graphene.Int(required=True)
    )
    all_playercards_of_a_team = graphene.List(
        PlayerCardNode, team_id=graphene.Int(required=True)
    )
    all_playercards_of_a_team_and_rarity = graphene.List(
        PlayerCardNode,
        team_id=graphene.Int(required=True),
        cardrarity_name=graphene.String(required=True),
    )
    all_playercards_of_a_user = graphene.List(
        PlayerCardNode, user_id=graphene.Int(required=True)
    )
    all_playercards_of_the_current_user = graphene.List(PlayerCardNode)
    cardrarity = graphene.Field(CardRarityType, id=graphene.Int(required=True))
    all_cardrarities = graphene.List(CardRarityType)

    def resolve_playercard(root, info, id):
        return PlayerCard.objects.get(id=id)

    def resolve_all_playercards(root, info, **kwargs):
        return playercards_queryset

    def resolve_all_playercards_of_a_cardrarity(root, info, cardrarity_id):
        return playercards_queryset.filter(rarity_id=cardrarity_id)

    def resolve_all_playercards_of_a_player(root, info, player_id):
        return PlayerCard.objects.filter(player_id=player_id)

    def resolve_all_playercards_of_a_team(root, info, team_id):
        return PlayerCard.objects.filter(player__team_id=team_id)

    def resolve_all_playercards_of_a_team_and_rarity(
        root, info, team_id, cardrarity_name
    ):
        return PlayerCard.objects.filter(
            player__team_id=team_id, rarity__name=cardrarity_name
        )

    def resolve_all_playercards_of_a_user(root, info, user_id):
        return PlayerCard.objects.filter(owner_id=user_id)

    def resolve_all_playercards_of_the_current_user(root, info):
        user = info.context.user
        if user.is_anonymous:
            return PlayerCard.objects.none()
        else:
            return PlayerCard.objects.filter(owner_id=user.id)

    def resolve_cardrarity(root, info, id):
        return CardRarity.objects.get(id=id)

    def resolve_all_cardrarities(root, info, **kwargs):
        return CardRarity.objects.all()
