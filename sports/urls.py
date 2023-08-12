from django.urls import path, include


app_name = "sports"

urlpatterns = [
    path("basketball/", include("sports.basketball.urls", namespace="basketball")),
    path("football/", include("sports.football.urls", namespace="football")),

]
