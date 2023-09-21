from django.contrib import admin
from .models import CardRarity, PlayerCard, PlayerCardLike, BundleCard, Bundle, TeamCollection

# Register your models here.

class TeamCollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "rarity_name", "reward_id", "team")
    list_filter = ("rarity_name", "team")
    search_fields = ("name", "description")
    readonly_fields = ("reward_id","cards")

class PlayerCardAdmin(admin.ModelAdmin):
    list_display = ("player", "rarity", "owner", "for_sale", "price")
    list_filter = ("rarity", "for_sale", "price")
    search_fields = ("player",)
    readonly_fields = ("slug",)
    
admin.site.register(TeamCollection, TeamCollectionAdmin)
admin.site.register(CardRarity)
admin.site.register(PlayerCard, PlayerCardAdmin)
admin.site.register(PlayerCardLike)
admin.site.register(BundleCard)
admin.site.register(Bundle)