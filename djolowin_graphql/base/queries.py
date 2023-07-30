import graphene

from base.models import Team, Player, Country
from .types import TeamType, PlayerType, CountryType

class BaseQueries(graphene.ObjectType):
    team = graphene.Field(TeamType, id=graphene.Int(required=True))
    all_teams = graphene.List(TeamType)
    player = graphene.Field(PlayerType, id=graphene.Int(required=True))
    all_players = graphene.List(PlayerType)
    all_players_of_a_team = graphene.List(PlayerType, team_id=graphene.Int(required=True))
    country = graphene.Field(CountryType, id=graphene.Int(required=True))
    all_countries = graphene.List(CountryType)

    def resolve_team(root, info, id):
        """Get team by id"""
        return Team.objects.get(id=id)
    
    def resolve_all_teams(root, info, **kwargs):
        """Get all teams"""
        return Team.objects.all()
    
    def resolve_player(root, info, id):
        """Get player by id"""
        return Player.objects.get(id=id)
    
    def resolve_all_players(root, info, **kwargs):
        """Get all players"""
        return Player.objects.all()
    
    def resolve_all_players_of_a_team(root, info, team_id):
        """ Get all players of a team"""
        return Player.objects.filter(team_id=team_id)
    
    def resolve_country(root, info, id):
        """Get country by id"""
        return Country.objects.get(id=id)
    
    def resolve_all_countries(root, info, **kwargs):
        """Get all countries"""
        return Country.objects.all()