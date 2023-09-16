from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import CardAuction
from shared_models.models import PlayerCard

@api_view(["POST"])
def auction_expired_webhook(request):
        auction_id = request.data.get("auction_id")
        # Check if auction exists
        try:
            auction = CardAuction.objects.get(pk=auction_id)
        except CardAuction.DoesNotExist:
            return Response({"message": "The Auction does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # Check if auction has been marked as sold
        if auction.sold or auction.auction_complete:
            return Response({"message": "Auction already processed"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if auction has expired
        if not auction.has_expired:
            return Response({"message": "Auction has not ended"}, status=status.HTTP_400_BAD_REQUEST)
        card = PlayerCard.objects.get(pk=auction.card_id)
        # If no bids, end auction and unlock card
        if auction.get_highest_bid() is None:
            card.is_locked = False
            auction.auction_complete = True
            auction.save()
            return Response({"message": "Auction processed succesfully"}, status=status.HTTP_200_OK)
        # If bids, mark as sold and lock card
        highest_bid = auction.get_highest_bid()
        winner_id = highest_bid.bidder_id
        card.owner_id = winner_id
        card.is_locked = False
        card.save()
        auction.sold = True
        auction.auction_complete = True
        auction.save()
        return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
def check_auction_existence(request, card_id):
    # Check if auction exists
    try:
        auction = CardAuction.objects.get(Q(card_id=card_id) & Q(auction_complete=False))
    except CardAuction.DoesNotExist:
        return Response({"message": False}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": True, "auction_id":auction.id}, status=status.HTTP_200_OK)