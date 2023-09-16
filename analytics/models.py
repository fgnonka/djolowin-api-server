from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField

from . import CustomerEvents, AuctionEvents, InAppCurrencyEvents


class CustomerEvent(models.Model):
    """Records events that happened during the customer lifecycle."""

    initiator = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(
        _("Date"),
        auto_now_add=True,
    )
    event_type = models.CharField(
        _("Event type"),
        max_length=255,
        choices=CustomerEvents.CHOICES,
    )
    user_id = models.IntegerField(_("User ID"), blank=True, null=True)
    payload = JSONField(_("Event parameters"), blank=True, default=dict, null=True)

    class Meta:
        ordering = ("-date",)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.event_type!r}, user={self.user_id!r})"

    def __str__(self):
        return f"{self.event_type} - {self.user_id} - {self.date.strftime('%-d %B %Y, %I:%M:%S%p')} - {self.initiator}"


class AuctionEvent(models.Model):
    """Records events that happened during the auction lifecycle."""

    initiator = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(
        _("Date"),
        auto_now_add=True,
    )
    event_type = models.CharField(
        _("Event type"),
        max_length=255,
        choices=AuctionEvents.CHOICES,
    )
    auction_id = models.IntegerField(_("Auction ID"), blank=True, null=True)
    payload = JSONField(_("Event parameters"), blank=True, default=dict, null=True)

    class Meta:
        ordering = ("-date",)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.event_type!r}, auction={self.auction_id!r})"

    def __str__(self):
        return f"{self.event_type} - {self.auction_id} - {self.date.strftime('%-d %B %Y, %I:%M:%S%p')} - {self.initiator}"


class InAppCurrencyEvent(models.Model):
    """Records events that happened during the app currency lifecycle."""

    initiator = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(
        _("Date"),
        auto_now_add=True,
    )
    event_type = models.CharField(
        _("Event type"),
        max_length=255,
        choices=InAppCurrencyEvents.CHOICES,
    )
    user_id = models.IntegerField(_("User ID"), blank=True, null=True)
    payload = JSONField(_("Event parameters"), blank=True, default=dict, null=True)

    class Meta:
        ordering = ("-date",)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.event_type!r}, user={self.user_id!r})"

    def __str__(self):
        return f"{self.event_type} - {self.user_id} - {self.date.strftime('%-d %B %Y, %I:%M:%S%p')} - {self.initiator}"
