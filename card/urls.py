from django.urls import path

from .views import (
    PlayerCardDetailAPIView,
    PlayerCardListAPIView,
    OwnedPlayerCardListAPIView
)

app_name = "card"

urlpatterns = [
    path("all/", PlayerCardListAPIView.as_view(), name="all"),
    path("owned/", OwnedPlayerCardListAPIView.as_view(), name="owned"),
    path("<slug:slug>/", PlayerCardDetailAPIView.as_view(), name="detail"),
]
