from django.urls import path, reverse_lazy
from .views import (
    LeagueListAPIView,
    LeagueDetailAPIView,
    TeamListAPIView,
    TeamDetailAPIView,
    PlayerListByTeamApiView,
    PlayerDetailAPIView

)

app_name = "football"

urlpatterns = [
    path("leagues/", LeagueListAPIView.as_view(), name="league-list"),
    path("league/<slug:slug>/", LeagueDetailAPIView.as_view(), name="league-detail"),
    path("teams/", TeamListAPIView.as_view(), name="team-list"),
    path("team/<slug:slug>/", TeamDetailAPIView.as_view(), name="team-detail"),
    path("team/<slug:slug>/players/", PlayerListByTeamApiView.as_view(), name="player-list"),
    path("player/<slug:slug>/", PlayerDetailAPIView.as_view(), name="player-detail"),
]