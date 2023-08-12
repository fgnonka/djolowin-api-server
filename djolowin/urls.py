from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls", namespace="account")),
    path("auction/", include("auction.urls", namespace="auction")),
    path("card/", include("card.urls", namespace="card")),
    path("currency/", include("app_currency.urls", namespace="currency")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True)), name="api"),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("sports/", include("sports.urls", namespace="sports")),
    path("transaction/", include("transaction.urls", namespace="transaction")),
    path("wallet/", include("wallet.urls", namespace="wallet")),
]

urlpatterns += staticfiles_urlpatterns()

