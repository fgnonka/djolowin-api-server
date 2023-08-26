import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model
from promise import Promise


from accounts import models


class AddressType(DjangoObjectType):
    class Meta:
        description = "Represents user address data."
        model = models.Address
        fields = "__all__"


class CustomUserType(DjangoObjectType):
    class Meta:
        description = "Represents user data."
        model = models.CustomUser
        fields = "__all__"
