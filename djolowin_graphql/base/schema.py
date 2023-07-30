import graphene

from .queries import BaseQueries

schema = graphene.Schema(query=BaseQueries)