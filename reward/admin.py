from django.contrib import admin

from .models import DJOBAReward

class DJOBARewardAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "amount", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")

admin.site.register(DJOBAReward, DJOBARewardAdmin)