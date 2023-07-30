from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import DjolowinProfileView

app_name = "djolowin_profile"

urlpatterns = [
    path("", cache_page(60*10)(DjolowinProfileView.as_view()), name="profile")
]
