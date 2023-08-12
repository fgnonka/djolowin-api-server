from django.contrib import admin
from .models import CardRarity, PlayerCard, PlayerCardLike, BundleCard, Bundle

# Register your models here.
admin.site.register(CardRarity)
admin.site.register(PlayerCard)
admin.site.register(PlayerCardLike)
admin.site.register(BundleCard)
admin.site.register(Bundle)