import graphene
from graphene_django import DjangoObjectType

from base.models import Team, Player, Country

class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        fields = "__all__"


class PlayerType(DjangoObjectType):
    age = graphene.Int()
    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "position",
            "date_of_birth",
            "jersey_number",
            "image",
            "team",
            "country",
            "slug",
            "age",
        )
    def resolve_age(self, info):
        return self.get_player_age

class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = "__all__"