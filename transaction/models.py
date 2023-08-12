from django.conf import settings
from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("card_purchase", "Card Purchase"),
        ("bundle_purchase", "Bundle Purchase"),
    )

    buyer_id = models.IntegerField()
    buyer_name = models.CharField(max_length=100)
    seller_id = models.IntegerField(null=True, blank=True)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    card_id = models.IntegerField(null=True, blank=True)
    bundle_id = models.IntegerField(null=True, blank=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.transaction_type == "card_purchase":
            return f"{self.buyer_name} - {self.card_id} - {self.timestamp.__format__('%Y-%m-%d %H:%M:%S')}"
        else:
            return f"{self.buyer_name} - {self.bundle_id} - {self.timestamp.__format__('%Y-%m-%d %H:%M:%S')}"

    

class InAppCurrencyTransaction(models.Model):
    user_id = models.IntegerField()
    currency_package_id = models.IntegerField()
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    currency_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.currency_package_id} - {self.timestamp.__format__('%Y-%m-%d %H:%M:%S')}"


class AuctionTransaction(models.Model):
    seller_id = models.IntegerField()
    winner_id = models.IntegerField(null=True, blank=True)
    auction_id = models.IntegerField()
    start_price = models.PositiveIntegerField()
    winning_bid = models.PositiveIntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    number_of_bids = models.PositiveIntegerField(default=0)
    number_of_watchers = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Auction by {self.seller.username} - {self.auction.card} - {self.start_time.__format__('%Y-%m-%d %H:%M:%S')} - {self.end_time.__format__('%Y-%m-%d %H:%M:%S')}"
