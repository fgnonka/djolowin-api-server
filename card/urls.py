from django.urls import path

from .views import (
    PlayerCardDetailAPIView,
    PlayerCardListAPIView,
    OwnedPlayerCardListAPIView,
    PurchaseCardView
)

app_name = "card"

urlpatterns = [
    path("all/", PlayerCardListAPIView.as_view(), name="all"),
    path("owned/", OwnedPlayerCardListAPIView.as_view(), name="owned"),
    path("<slug:slug>/", PlayerCardDetailAPIView.as_view(), name="detail"),
    path("purchase/<int:id>/", PurchaseCardView.as_view(), name="purchase"),
]