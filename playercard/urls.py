from django.urls import path
from django.views.decorators.cache import cache_page

from .api_views import PlayerCardsList, CardRarityList, Login
from . import views
from .dynamic import search_player_cards



app_name = "playercard"

urlpatterns = [
    path("api/playercards/", PlayerCardsList.as_view(), name="playercards"),
    path("api/cardrarity/", CardRarityList.as_view(), name="cardrarities"),
    path("api/login/", Login.as_view(), name="login"),
    path(
        "owned/",
        cache_page(60*2)(views.UserPlayerCardListView.as_view()),
        name="owned-playercard",
    ),
    path(
        "all/",
        cache_page(60*2)(views.PlayerCardListView.as_view()),
        name="playercard-list",
    ),
    path(
        "card/<int:pk>/",
        cache_page(60*2)(views.PlayerCardDetailView.as_view()),
        name="playercard-detail",
    ),
    path('card/<int:pk>/update-price/', views.UpdatePlayerCardView.as_view(), name='update_price'),
    path(
        "team/<str:slug>/", views.playercards_by_team_list, name="playercards-by-team"
    ),    
    path("purchase/<int:pk>/", views.purchase_playercard, name="purchase-playercard"),
    path('search_playercards/', search_player_cards, name='search_playercards'),
    path('card_rarity_list/', views.CardRarityListView.as_view(), name='card_rarity_list'),
]
