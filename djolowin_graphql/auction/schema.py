import graphene

from .queries import AuctionQueries



schema = graphene.Schema(query=AuctionQueries)
