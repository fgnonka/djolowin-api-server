from django.contrib import admin
from .models import CardAuction, CardAuctionBid, CardAuctionWatcher

# Register your models here.

class CardAuctionAdmin(admin.ModelAdmin):
    list_display = ("card", "seller", "starting_price", "current_bid", "highest_bidder", "start_time", "duration", "end_time", "auction_complete", "sold", "timestamp")
    list_filter = ("auction_complete", "sold")
    search_fields = ("card", "seller", "highest_bidder")
    readonly_fields = ("card", "start_time", "end_time", "timestamp")

admin.site.register(CardAuction, CardAuctionAdmin)
admin.site.register(CardAuctionBid)
admin.site.register(CardAuctionWatcher)