from django.contrib import admin
from .models import CustomUser, UserWallet, CustomerEvent

admin.site.register(CustomUser)


class UserWalletAdmin(admin.ModelAdmin):
    list_display = ("user_id", "balance", "reserved_balance", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user_id", "balance", "reserved_balance", "created_at", "updated_at")
    
    def get_readonly_fields(self, request, obj=None):
        # Make the "user_id" field read-only for both add and change views
        return ["user_id"]

class CustomerEventAdmin(admin.ModelAdmin):
    list_display = ("user_id", "event_type", "initiator", "payload", "date")
    list_filter = ("event_type", "date")
    search_fields = ("user_id", "event_type", "initiator", "payload", "date")


admin.site.register(CustomerEvent, CustomerEventAdmin)
admin.site.register(UserWallet, UserWalletAdmin)
