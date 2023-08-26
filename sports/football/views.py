from rest_framework import generics

from ..serializers import (
    LeagueSerializer,
    TeamSerializer,
    PlayerSerializer
)
from ..models import League, Team, Player
# Create your views here.

class LeagueListAPIView(generics.ListAPIView):
    queryset = League.objects.filter(sport="football")
    serializer_class = LeagueSerializer

class LeagueDetailAPIView(generics.RetrieveAPIView):
    queryset = League.objects.filter(sport="football")
    serializer_class = LeagueSerializer

    def get_object(self):
        league =  League.objects.get(slug=self.kwargs["slug"])
        team_list = Team.objects.filter(league=league)
        league.teams = team_list
        return league
    

class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.filter(sport="football")
    serializer_class = TeamSerializer

class TeamDetailAPIView(generics.RetrieveAPIView):
    queryset = Team.objects.filter(sport="football")
    serializer_class = TeamSerializer
    
    def get_object(self):
        team = Team.objects.get(slug=self.kwargs["slug"])
        player_list = Player.objects.filter(team=team)
        team.players = player_list
        return team

class PlayerListByTeamApiView(generics.ListAPIView):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

    def get_queryset(self):
        return Player.objects.filter(team__slug=self.kwargs["slug"])

class PlayerDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

    def get_object(self):
        return Player.objects.get(slug=self.kwargs["slug"])