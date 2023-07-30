from graphene_django.types import DjangoObjectType

from auction.models import Auction, Bid


class AuctionType(DjangoObjectType):
    class Meta:
        model = Auction
        fields = "__all__"

class BidType(DjangoObjectType):
    class Meta:
        model = Bid
        fields = "__all__"
