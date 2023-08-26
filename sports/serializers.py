from rest_framework import serializers
from .models import League, Team, Player


class PlayerSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    league_name = serializers.SerializerMethodField()
    
    def get_league_name(self, obj):
        return obj.team.league.name
    
    def get_team_name(self, obj):
        return obj.team.name
    
    def get_age(self, obj):
        return obj.get_player_age
    
    class Meta:
        model = Player
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class LeagueSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    class Meta:
        model = League
        fields = "__all__"
