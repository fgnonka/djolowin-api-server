from django.urls import path
from .views import (
    CardAuctionDetailView,
    CreateCardAuctionView,
    ActiveCardAuctionListView,
    OwnedCardAuctionListView,
)

app_name = "auction"

urlpatterns = [
    path("all/", ActiveCardAuctionListView.as_view(), name="all_auctions"),
    path("create/", CreateCardAuctionView.as_view(), name="create_auction"),
    path("<int:pk>/", CardAuctionDetailView.as_view(), name="auction_detail"),
    path("owned/", OwnedCardAuctionListView.as_view(), name="owned_auctions"),
]
