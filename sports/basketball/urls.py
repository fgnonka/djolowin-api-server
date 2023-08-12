from django.urls import path, reverse_lazy
from .views import (
    LeagueListAPIView,
    LeagueDetailAPIView,
    TeamListAPIView,
    TeamDetailAPIView,

)

app_name = "basketball"

urlpatterns = [
    path("leagues/", LeagueListAPIView.as_view(), name="league-list"),
    path("leagues/<slug:slug>/", LeagueDetailAPIView.as_view(), name="league-detail"),
    path("teams/", TeamListAPIView.as_view(), name="team-list"),
    path("teams/<slug:slug>/", TeamDetailAPIView.as_view(), name="team-detail"),
]