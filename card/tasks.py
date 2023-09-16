from celery import shared_task

from .models import PlayerCard

@shared_task
def transfer_card_ownership(card_id, new_owner_id):
    card = PlayerCard.objects.get(id=card_id)
    card.owner_id = new_owner_id
    card.is_locked = False
    card.save()