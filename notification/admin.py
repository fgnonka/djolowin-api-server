from django.contrib import admin

from .models import NotificationPreferences
# Register your models here.


class NotificationPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user_id',)
    list_filter = ('user_id',)
    search_fields = ('user_id',)

admin.site.register(NotificationPreferences, NotificationPreferencesAdmin)