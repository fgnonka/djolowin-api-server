from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("custom_user.urls", namespace="custom_user")),
    path("auction/", include("auction.urls", namespace="auction")),
    path("card/", include("card.urls", namespace="card")),
    path("currency/", include("app_currency.urls", namespace="currency")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="api"),
    path("sports/", include("sports.urls", namespace="sports")),
    path("transaction/", include("transaction.urls", namespace="transaction")),
]

urlpatterns += staticfiles_urlpatterns()
