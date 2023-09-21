import random
from django.db.models import Q

from. models import PlayerCard, CardRarity

def extract_player_query_params(self):
    if "player_name" not in self.request.query_params:
        return None
    player_query = Q()  # Create an empty Q object for player filtering
    try:
        player_name = self.request.query_params["player_name"]
        player_query &= Q(player__name__icontains=player_name)
    except KeyError:
        player_name = None
    return player_query

def extract_rarity_query_params(self):
    if "rarity" not in self.request.query_params:
        return None
    rarity_queries = Q()  # Create an empty Q object for rarity filtering
    try:
        rarity_names = self.request.query_params.getlist("rarity")
        for rarity_name in rarity_names:
            print(rarity_name)
            rarity = CardRarity.objects.get(name=rarity_name)
            rarity_queries |= Q(rarity=rarity)
    except KeyError:
        rarity_names = None
    return rarity_queries
            

class FilterMixin:
    def filter_all_cards(self):
        """ Filter all cards based on rarity and player name"""
        filter_conditions = Q()
        queryset = PlayerCard.objects.filter(for_sale=True)
        
        player_query = extract_player_query_params(self)
        rarity_queries = extract_rarity_query_params(self)
        # Use the Q object to build complex queries

        # Combine the player_name and rarity_queries using OR (|) operator
        if rarity_queries is not None:
            filter_conditions |= rarity_queries
        if player_query is not None:
            filter_conditions &= player_query
            
        queryset = queryset.filter(filter_conditions)
        return queryset
    
    def filter_owned_cards(self):
        filter_conditions = Q()
        queryset = PlayerCard.objects.filter(owner=self.request.user)
        
        player_query = extract_player_query_params(self)
        rarity_queries = extract_rarity_query_params(self)
        
        if player_query is not None:
            filter_conditions &= player_query
        if rarity_queries is not None:
            filter_conditions |= rarity_queries
        queryset = queryset.filter(filter_conditions)
        return queryset
        