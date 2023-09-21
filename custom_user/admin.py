from django.contrib import admin
from .models import CustomUser, UserWallet, CustomerEvent, Address
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_joined", "last_login", "is_active", "is_staff", "is_verified")
    search_fields = ("username", "email")
    list_filter = ("date_joined", "last_login")
    readonly_fields = (
        "username",
        "email",
        "date_joined",
        "last_login",
        'password',
        # Add more fields you want to make read-only here
    )


class UserWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "reserved_balance", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user", "balance", "reserved_balance", "created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        # Make the "user" field read-only for both add and change views
        return ["user"]


class CustomerEventAdmin(admin.ModelAdmin):
    list_display = ("user_id", "event_type", "initiator", "payload", "date")
    list_filter = ("event_type", "date")
    search_fields = ("user_id", "event_type", "initiator", "payload", "date")


class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "street_address", "city", "country", "postal_code")
    list_filter = ("country",)
    search_fields = ("user", "street_address", "city", "country", "postal_code")


admin.site.register(Address, AddressAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomerEvent, CustomerEventAdmin)
admin.site.register(UserWallet, UserWalletAdmin)
