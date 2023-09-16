from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse
from django.utils import timezone

from . import AuctionEvents
from custom_user.models import CustomUser
from card.models import PlayerCard


class CardAuctionWatcher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey("CardAuction", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class CardAuction(models.Model):
    card = models.ForeignKey(PlayerCard, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    starting_price = models.PositiveIntegerField(validators=[MinValueValidator(2000)])
    current_bid = models.PositiveIntegerField(default=0)
    highest_bidder = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="highest_bidder",
    )
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(default=1)
    end_time = models.DateTimeField()
    watchers = models.ManyToManyField(
        CardAuctionWatcher, blank=True, related_name="watchers"
    )
    auction_complete = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-start_time"]
        constraints = [
            UniqueConstraint(
                fields=["card_id", "seller_id", "start_time"], name="unique_auction"
            )
        ]

    @property
    def get_auction_details(self):
        seller_name = self.seller.username
        number_bids = CardAuctionBid.objects.filter(auction=self).count()
        return {
            "seller_name": seller_name,
            "number_bids": number_bids,
        }

    @property
    def get_card_details(self):
        details = self.card.get_card_details
        return details

    @property
    def already_active(self):
        existing_active_auction = CardAuction.objects.filter(
            Q(card=self.card) & Q(seller=self.seller) & Q(end_time__gte=timezone.now())
        )
        if existing_active_auction:
            return True
        else:
            return False

    @property
    def is_ending_soon(self):
        now = timezone.now()
        delta = timezone.timedelta(minutes=15)
        return self.end_time <= now + delta

    @property
    def has_expired(self):
        now = timezone.now()
        return self.end_time <= now

    def save(self, *args, **kwargs):
        if self.pk is None:
            duration_in_delta = timezone.timedelta(hours=self.duration)
            print(duration_in_delta)
            start_time = timezone.now()
            self.end_time = start_time + duration_in_delta
            self.timestamp = timezone.now()
        super().save(*args, **kwargs)

    def mark_as_sold(self):
        self.sold = True
        self.save()

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now and self.end_time >= now

    def __str__(self):
        return f"{self.card} - Sold by {self.seller}"

    def get_absolute_url(self):
        return reverse("auction:auction_detail", kwargs={"pk": self.pk})

    def get_highest_bid(self):
        if self.current_bid:
            return (
                CardAuctionBid.objects.filter(auction=self).order_by("-amount").first()
            )


class CardAuctionBid(models.Model):
    auction = models.ForeignKey(CardAuction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bidder"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.name} - Bid on: {self.auction} for {self.amount:,} DJOBA"

    def save(self, *args, **kwargs):
        if self.auction.is_active():
            super().save(*args, **kwargs)
        else:
            raise Exception("Auction is not active.")

    def get_absolute_url(self):
        return reverse("auction:auction_detail", kwargs={"pk": self.auction.pk})


class CardAuctionEvent(models.Model):
    """Records events that occur during an auction."""

    seller_id = models.PositiveIntegerField()
    winner_id = models.PositiveIntegerField(null=True, blank=True)
    auction = models.ForeignKey(CardAuction, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255, choices=AuctionEvents.CHOICES)
    payload = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.event_type} - {self.auction}"
