import graphene
from .account.schema import AccountMutations, AccountQueries
from .auction.schema import AuctionQueries
from .base.schema import BaseQueries
from .playercard.schema import PlayerCardQueries


class Mutation(AccountMutations, graphene.ObjectType):
    pass


class Query(
    AccountQueries, AuctionQueries, BaseQueries, PlayerCardQueries, graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
