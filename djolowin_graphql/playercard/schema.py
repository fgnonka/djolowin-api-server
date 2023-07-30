import graphene

from .queries import PlayerCardQueries



schema = graphene.Schema(query=PlayerCardQueries)