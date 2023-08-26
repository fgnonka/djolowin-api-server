from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import F

from custom_user.models import UserWallet
from .models import PlayerCard

def purchase_card_action(card_id, buyer_id):
    try:
        with transaction.atomic():
            card = get_object_or_404(PlayerCard, id=card_id)
            # Check if card is for sale and not owned by buyer himself
            if card.for_sale == False or card.owner_id == buyer_id:
                return False, "Card is not for sale"
            
            # Check if buyer has enough balance to purchase card
            buyer_wallet = get_object_or_404(UserWallet, user_id=buyer_id)
            available_balance = buyer_wallet.available_balance
            
            if available_balance < card.value:
                return False, "Insufficient balance"
            else:
                
                # If card is owned by someone else, transfer the ammount to the owner
                if card.owner_id:
                    seller_wallet = get_object_or_404(UserWallet, user_id=card.owner_id)
                    seller_wallet.balance = F('balance') + card.value
                    seller_wallet.save()
                
                # Deduct the card price from the buyer's balance
                buyer_wallet.balance = F('balance') - card.value
                buyer_wallet.save()
                
                # Update card ownership and status
                card.owner_id = buyer_id
                card.for_sale = False
                card.save()
                
                return True, "Card purchased successfully"
    except Exception as e:
        return False, str(e)