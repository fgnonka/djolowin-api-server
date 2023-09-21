import random

from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .card_purchase import purchase_card_action
from .forms import CardForm
from . import kafka_producers
from .mixins import FilterMixin
from .models import PlayerCard, TeamCollection, CardRarity
from .pagination import CustomPagination
from .serializers import PlayerCardSerializer, TeamCollectionSerializer

# Create your views here.


class OwnedPlayerCardListAPIView(generics.ListAPIView, FilterMixin):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.request.user.id
        if user_id is not None:
            queryset = self.filter_owned_cards()
        return queryset


class PlayerCardListAPIView(generics.ListAPIView, FilterMixin):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    pagination_class = CustomPagination
    
    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.filter_all_cards()
        all_rows = list(queryset)
        random.shuffle(all_rows)
        return all_rows


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
                {"message": "This card does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PlayerCardSerializer(selected_card)
        is_owned_by_user = selected_card.owner_id == request.user.id
        return Response({"is_owned_by_me": is_owned_by_user, "data": serializer.data,},  status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        print(request.data)
        # Retrieve the PlayerCard instance
        selected_card = self.get_object()
        # Check if the user making the request is the owner of the card
        if selected_card.owner_id != request.user.id:
            return Response(
                {"message": "You are not the owner of this card."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Check if the card is locked (if it is, it cannot be updated)
        if selected_card.is_locked:
            return Response(
                {"message": "This card is locked and cannot be updated."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Update the card
        form = CardForm(data=request.data)
        if form.is_valid():
            if form.cleaned_data["price"] != selected_card.price:
                selected_card.price = form.cleaned_data["price"]
                
                # Kafka event "card_price_updated" is sent here
                kafka_producers.kafka_card_price_updated_event(selected_card.id)
            if selected_card.for_sale == False and form.cleaned_data["for_sale"] == True:
                selected_card.for_sale = form.cleaned_data["for_sale"]
                
                # Kafka event "card_marked_for_sale" is sent here
                kafka_producers.kafka_card_marked_for_sale_event(selected_card.id)
            selected_card.save()
            return Response(
                {"message": "Card updated successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Please check the data you have entered."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PurchaseCardView(generics.RetrieveUpdateAPIView):
    queryset = PlayerCard.objects.all()
    serializer_class = PlayerCardSerializer
    lookup_field = "id" # This is the primary key of the card

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
                    
                    # Kafka event "card_purchased" is sent here
                    kafka_producers.kafka_card_purchased_event(card.id)
                    return Response({'message': message}, status=status.HTTP_200_OK)
                else:
                    
                    # Kafka event "card_purchase_failed" is sent here
                    kafka_producers.kafka_card_purchase_failed_event(card.id)
                    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeamCollectionListAPIView(generics.ListAPIView):
    queryset = TeamCollection.objects.all()
    serializer_class = TeamCollectionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = TeamCollection.objects.all()
        user_id = self.request.user.id
        if user_id is not None:
            queryset = queryset.filter(owner_id=user_id)
        return queryset