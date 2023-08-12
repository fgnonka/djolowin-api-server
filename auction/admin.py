from django.contrib import admin
from .models import CardAuction, CardAuctionBid, CardAuctionWatcher

# Register your models here.

admin.site.register(CardAuction)
admin.site.register(CardAuctionBid)
admin.site.register(CardAuctionWatcher)