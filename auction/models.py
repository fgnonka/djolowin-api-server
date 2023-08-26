from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse
from django.utils import timezone

from shared_models.models import PlayerCard

class CardAuctionWatcher(models.Model):
    user_id = models.IntegerField()
    auction = models.ForeignKey("CardAuction", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class CardAuction(models.Model):
    card_id = models.IntegerField()
    seller_id = models.IntegerField()
    starting_price = models.PositiveIntegerField(validators=[MinValueValidator(2000)])
    current_bid = models.PositiveIntegerField(default=0)
    highest_bidder = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(default=1)
    end_time = models.DateTimeField()
    watchers = models.ManyToManyField(CardAuctionWatcher, blank=True, related_name="watchers")
    auction_ended = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ["-start_time"]
        constraints = [
            UniqueConstraint(fields=["card_id", "seller_id","start_time"], name="unique_auction")
        ]
        
    @property
    def get_card_details(self):
        card = PlayerCard.objects.get(pk=self.card_id)
        details = card.get_card_details
        return details
    
    @property
    def already_active(self):
        existing_active_auction = CardAuction.objects.filter(
            Q(card=self.card) & Q(owner=self.owner) & Q(end_time__gte=timezone.now())
        )
        if existing_active_auction:
            return True
        else:
            return False

    @property
    def has_ended(self):
        now = timezone.now()
        return self.end_time <= now

    @property
    def is_ending_soon(self):
        now = timezone.now()
        return self.end_time - now < timezone.timedelta(hours=1)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            duration_in_delta = timezone.timedelta(hours=self.duration)
            print(duration_in_delta)
            start_time = timezone.now()
            self.end_time = start_time + duration_in_delta
        super().save(*args, **kwargs)
    
    def is_active(self):
        now = timezone.now()
        return self.start_time <= now and self.end_time >= now

    def __str__(self):
        return f"{self.card_id} - Auction by {self.seller_id}"

    
    def get_absolute_url(self):
        return reverse("auction:auction_detail", kwargs={"pk": self.pk})

    def get_highest_bid(self):
        if self.current_bid:
            return CardAuctionBid.objects.filter(auction=self).order_by("-amount").first()


class CardAuctionBid(models.Model):
    auction = models.ForeignKey(CardAuction, on_delete=models.CASCADE)
    bidder_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - Bid on: {self.auction} for {self.amount:,} DJOBA"

    def save(self, *args, **kwargs):
        if self.auction.is_active():
            super().save(*args, **kwargs)
        else:
            raise Exception("Auction is not active.")
    
    def get_absolute_url(self):
        return reverse("auction:auction_detail", kwargs={"pk": self.auction.pk})
