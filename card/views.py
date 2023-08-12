from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .forms import CardForm
from .models import PlayerCard
from .pagination import CustomPagination
from .serializers import PlayerCardSerializer

# Create your views here.


class OwnedPlayerCardListAPIView(generics.ListAPIView):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PlayerCard.objects.all()
        user_id = self.request.query_params.get("user_id", None)
        if user_id is not None:
            queryset = queryset.filter(owner_id=user_id)
        return queryset


class PlayerCardListAPIView(generics.ListAPIView):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PlayerCard.objects.all()
        player_name = self.request.query_params.get("player_name", None)
        if player_name is not None:
            queryset = queryset.filter(player_name=player_name)
        return queryset


class PlayerCardDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    lookup_field = "slug"

    def get_object(self):
        try:
            return PlayerCard.objects.get(slug=self.kwargs["slug"])
        except PlayerCard.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        # Retrieve the PlayerCard instance
        selected_card = self.get_object()
        # Check if the user making the request is the owner of the card
        if selected_card.owner != request.user:
            return Response(
                {"detail": "You are not the owner of this card."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Check if the card is locked (if it is, it cannot be updated)
        if selected_card.is_locked:
            return Response(
                {"detail": "This card is locked and cannot be updated."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Update the card
        form = CardForm(request.POST)
        if form.is_valid():
            selected_card.value = form.cleaned_data["value"]
            selected_card.for_sale = form.cleaned_data["for_sale"]
            selected_card.save()
        return Response(
            {"Message": "Card updated successfully."}, status=status.HTTP_200_OK
        )
