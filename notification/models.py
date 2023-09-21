from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class NotificationPreferences(models.Model):
    user_id = models.IntegerField(unique=True)
    # A user can choose to receive marketing emails from us.
    receive_email_updates = models.BooleanField(default=True)
    
    # A user can receive updates when a player they suscribed to is available for auction
    receive_player_available_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they have been outbid
    receive_outbid_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they have won an auction
    receive_winning_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they have successfully purchased a card
    receive_purchase_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they have successfully sold a card
    receive_sale_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they failed to sell a card
    receive_failed_sale_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they receive an offer for a card
    receive_offer_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they can claim a prize 
    receive_reward_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they can claim a referral reward
    receive_referral_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they can claim a loyalty reward
    receive_loyalty_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they can claim a birthday reward
    receive_birthday_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they can claim a milestone reward
    receive_milestone_updates = models.BooleanField(default=True)
    
    # A user can receive updates when they have completed a collection
    receive_collection_updates = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("User Preference")
        verbose_name_plural = _("User Preferences")

    def __str__(self):
        return f"Preference of {self.user_id}"
