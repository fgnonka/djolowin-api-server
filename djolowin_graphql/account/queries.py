import graphene

from accounts.models import CustomUser, Address
from core.exceptions import PermissionDenied
from graphql_auth.schema import UserQuery, MeQuery
from permission.auth_filters import AuthorizationFilters
from permission.enums import AccountPermissions

from .types import CustomUserType, AddressType


class AccountQueries(UserQuery, MeQuery, graphene.ObjectType):
    """Queries for Account"""

    
    user = graphene.Field(CustomUserType, id=graphene.Int(required=True))
    users_by_joined_date = graphene.List(
        CustomUserType, date_joined=graphene.Date(required=True)
    )
    address = graphene.Field(AddressType, id=graphene.Int(required=True))
    all_users = graphene.List(CustomUserType)
    all_staff = graphene.List(CustomUserType)
    all_addresses = graphene.List(AddressType)
    
    def resolve_user(root, info, id):
            """Get account by id"""
            return CustomUser.objects.get(id=id)
        
    def resolve_users_by_joined_date(root, info, date_joined):
        """Get all accounts ordered by date joined"""
        return CustomUser.objects.filter(date_joined__lte=date_joined)

    def resolve_all_users(root, info, **kwargs):
        """Get all accounts"""
        return CustomUser.objects.all()
    
    def resolve_all_staff(root, info, **kwargs):
        """Get all staff"""
        return CustomUser.objects.filter(is_staff=True)
    
    def resolve_address(root, info, id):
        """Get address by id"""
        return Address.objects.get(id=id)
    
    def resolve_addresses(root, info, **kwargs):
        """Get all addresses"""
        user = info.context.user
        if user:
            return Address.objects.filter(user=user)
        raise PermissionDenied(
            permissions=[AccountPermissions.MANAGE_USERS, AuthorizationFilters.OWNER]
        )
