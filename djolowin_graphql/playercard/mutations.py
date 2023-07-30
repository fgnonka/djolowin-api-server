import graphene

from playercard.models import CardRarity, PlayerCard

from .types import CardRarityType, PlayerCardType

class CreateCardRarity(graphene.Mutation):
    """Mutation to create a CardRarity"""

    class Arguments:
        name = graphene.String(required=True)

    cardrarity = graphene.Field(CardRarityType)

    @classmethod
    def mutate(cls, root, info, name):
        cardrarity = CardRarity.objects.create(name=name)
        return CreateCardRarity(cardrarity=cardrarity)


class UpdateCardRarity(graphene.Mutation):
    """Mutation to update a CardRarity"""

    cardrarity = graphene.Field(CardRarityType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()

    @staticmethod
    def mutate(cls, root, info, **data):
        cardrarity = CardRarity.objects.get(id=data["id"])

        cardrarity.name = data["name"]
        cardrarity.save()

        return UpdateCardRarity(cardrarity=cardrarity)