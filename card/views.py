from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .card_purchase import purchase_card_action
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
        user_id = self.request.user.id
        if user_id is not None:
            queryset = queryset.filter(owner_id=user_id)
        return queryset


class PlayerCardListAPIView(generics.ListAPIView):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PlayerCard.objects.filter(for_sale=True)
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
        
    def get(self, request, *args, **kwargs):
        selected_card = self.get_object()
        if selected_card is None:
            return Response(
                {"detail": "This card does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PlayerCardSerializer(selected_card)
        is_owned_by_user = selected_card.owner_id == request.user.id
        return Response({"is_owned_by_me": is_owned_by_user, "data": serializer.data,},  status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # Retrieve the PlayerCard instance
        selected_card = self.get_object()
        # Check if the user making the request is the owner of the card
        if selected_card.owner_id != request.user.id:
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
        form = CardForm(data=request.data)
        print(form)
        if form.is_valid():
            selected_card.value = form.cleaned_data["value"]
            selected_card.for_sale = form.cleaned_data["for_sale"]
            selected_card.save()
            return Response(
                {"detail": "Card updated successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Please check the data you have entered."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseCardView(generics.RetrieveUpdateAPIView):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    lookup_field = "id"  # Or "slug" if you're using slugs in your URL pattern

    def get_object(self):
        try:
            return PlayerCard.objects.get(id=self.kwargs["id"])
        except PlayerCard.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        try:
            card = self.get_object()
            if card is None:
                return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
            
            buyer_id = request.user.id  # Assuming you're using authentication

            with transaction.atomic():
                success, message = purchase_card_action(card.id, buyer_id)
                if success:
                    return Response({'message': message}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)