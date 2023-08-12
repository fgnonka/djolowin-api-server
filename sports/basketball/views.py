from rest_framework import generics

from ..serializers import (
    LeagueSerializer,
    TeamSerializer,
)
from ..models import League, Team
# Create your views here.

class LeagueListAPIView(generics.ListAPIView):
    queryset = League.objects.filter(sport="basketball")
    serializer_class = LeagueSerializer

class LeagueDetailAPIView(generics.RetrieveAPIView):
    queryset = League.objects.filter(sport="basketball")
    serializer_class = LeagueSerializer

    def get_object(self):
        return League.objects.get(slug=self.kwargs["slug"])

class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.filter(sport="basketball")
    serializer_class = TeamSerializer

class TeamDetailAPIView(generics.RetrieveAPIView):
    queryset = Team.objects.filter(sport="basketball")
    serializer_class = TeamSerializer
    
    def get_object(self):
        return Team.objects.get(slug=self.kwargs["slug"])