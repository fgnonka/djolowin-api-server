from django.urls import path

from .views import (
    BidListView,
    CardAuctionDetailView,
    CreateCardAuctionView,
    PlaceBidView,
    ActiveCardAuctionListView,
    OwnedCardAuctionListView,
)
from .webhooks import auction_expired_webhook, check_auction_existence

app_name = "auction"

urlpatterns = [
    path("all/", ActiveCardAuctionListView.as_view(), name="all_auctions"),
    path("bid/", PlaceBidView.as_view(), name="place_bid"),
    path("bids/<int:pk>/", BidListView.as_view(), name="bid_list"),
    path("create/", CreateCardAuctionView.as_view(), name="create_auction"),
    path("<int:pk>/", CardAuctionDetailView.as_view(), name="auction_detail"),
    path("owned/", OwnedCardAuctionListView.as_view(), name="owned_auctions"),
    path("webhook/auction_expiration/", auction_expired_webhook, name="auction_expired_webhook"),
    path("webhook/check_auction_existence/<int:card_id>", check_auction_existence, name="check_auction_existence"),
    
]
