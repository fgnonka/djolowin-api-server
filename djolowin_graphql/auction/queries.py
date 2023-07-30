import graphene

from auction.models import Auction, Bid
from core.exceptions import PermissionDenied
from permission.auth_filters import AuthorizationFilters
from permission.enums import AccountPermissions

from .types import AuctionType, BidType

class AuctionQueries(graphene.ObjectType):
    auction = graphene.Field(AuctionType, id=graphene.Int(required=True))
    all_auctions = graphene.List(AuctionType)
    all_active_auctions = graphene.List(AuctionType)
    all_auctions_of_a_user = graphene.List(AuctionType, user_id=graphene.Int(required=True))
    all_auctions_of_current_user = graphene.List(AuctionType)
    bid = graphene.Field(BidType, id=graphene.Int(required=True))
    all_bids_of_auction = graphene.List(BidType, auction_id=graphene.Int(required=True))
    
    
    def resolve_auction(root, info, id):
        """Get auction by id"""
        return Auction.objects.get(id=id)

    def resolve_all_auctions(root, info, **kwargs):
        """Get all auctions"""
        return Auction.objects.all()

    def resolve_all_active_auctions(root, info, **kwargs):
        """Get all active auctions"""
        return Auction.objects.filter(auction_ended=False)

    def resolve_all_auctions_of_a_user(root, info, user_id):
        """Get all auctions of a user"""
        return Auction.objects.filter(owner_id=user_id)

    def resolve_all_auctions_of_current_user(root, info, **kwargs):
        """Get all auctions of current user"""
        user = info.context.user
        if user:
            return Auction.objects.filter(owner=user)
        raise PermissionDenied(
            permissions=[AccountPermissions.MANAGE_USERS, AuthorizationFilters.OWNER]
        )

    def resolve_bid(root, info, id):
        """Get bid by id"""
        return Bid.objects.get(id=id)

    def resolve_all_bids_of_auction(root, info, auction_id):
        """Get all bids of an auction"""
        return Bid.objects.filter(auction_id=auction_id)
