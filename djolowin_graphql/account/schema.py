import graphene

from .mutations import AuthMutation
from .queries import AccountQueries


class AccountMutations(AuthMutation, graphene.ObjectType):
    """Mutations for Account"""

    pass


schema = graphene.Schema(query=AccountQueries, mutation=AccountMutations)
