from django.urls import path

from .views import NotificationPreferencesView

app_name = "notification"

urlpatterns = [
    path(
        "preferences/",
        NotificationPreferencesView.as_view(),
        name="notification-preferences",
    ),
]
