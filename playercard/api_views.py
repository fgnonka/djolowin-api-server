from django.contrib.auth import authenticate
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from .models import CardRarity, PlayerCard
from .serializers import CardRaritySerializer, PlayerCardSerializer


class Login(APIView):
    def post(self, request):
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if not user:
            return Response(
                {"error": "Credentials are incorrect or user does not exist"},
                status=HTTP_404_NOT_FOUND,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


class AllPlayerCardsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class PlayerCardsList(APIView):
    def get(self, request):
        queryset = PlayerCard.objects.all()
        paginator = AllPlayerCardsPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PlayerCardSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CardRarityList(APIView):
    def get(self, request):
        queryset = CardRarity.objects.all()
        serializer = CardRaritySerializer(queryset, many=True)
        return Response(serializer.data)
    
