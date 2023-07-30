from .enums import BasePermissionEnum

def is_user(context):
    user = context.user
    return user and user.is_active

def is_staff(context):
    return is_user(context) and context.user.is_staff

class AuthorizationFilters(BasePermissionEnum):
    #Grant access to authenticated user
    AUTHENTICATED_USER = "authorization_filters.authenticated_user"
    
    #Grant access to staff user
    AUTHENTICATED_STAFF_USER = "authorization_filters.authenticated_staff_user"
    
    #Grant access to owner of the related object
    OWNER = "authorization_filters.owner"