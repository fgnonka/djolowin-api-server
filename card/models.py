import uuid

from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from sports.models import Player, Team
from custom_user.models import CustomUser
# Create your models here.


class CardRarity(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @staticmethod
    def get_all_rarities():
        return CardRarity.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Card Rarity"
        verbose_name_plural = "Card Rarities"


class PlayerCard(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rarity = models.ForeignKey(
        CardRarity, on_delete=models.CASCADE, null=True, blank=True
    )
    season = models.CharField(_("Season"), max_length=10, default="2024")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    value = models.PositiveIntegerField(_("Value"))
    number_likes = models.PositiveIntegerField(_("Likes"), default=0)
    index = models.PositiveIntegerField(_("Index"), default=0)
    date_created = models.DateTimeField(
        _("Date created"), auto_now_add=True, db_index=True
    )
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)
    is_locked = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Player Card")
        verbose_name_plural = _("Player Cards")
        

    def __str__(self):
        return f"{self.rarity} - {self.player} - Index: {self.index}"

    def get_absolute_url(self):
        return reverse("card:playercard-detail", kwargs={"slug": self.pk})
    
    @property
    def get_card_details(self):
        details = {
            "card_id": self.pk,
            "player_id": self.player_id,
            "player_name": self.player.name,
            "rarity_name": self.rarity.name,
            "index": self.index,
            "season": self.season,
            "slug": self.slug,
        }
        return details
    
    
    @property
    def get_player_name(self):
        return self.player.name

    @property
    def card_rarity_name(self):
        return self.rarity.name

    @property
    def get_total_card_index(self):
        allcards = PlayerCard.objects.filter(
            Q(rarity=self.rarity) & Q(player_id=self.player_id) & ~Q(index=0)
        )
        return allcards.count()

    @staticmethod
    def get_all_cards():
        return PlayerCard.objects.all()

    def get_all_cards_by_player(self):
        return PlayerCard.objects.filter(player_id=self.player_id)

    def get_all_cards_by_owner(self):
        return PlayerCard.objects.filter(owner_id=self.owner_id)

    def get_number_of_cards(self):
        number_of_cards = PlayerCard.objects.filter(player_id=self.player_id).count()
        return number_of_cards

    def get_total_likes(self):
        return self.number_likes

    def get_card_owner(self):
        return self.owner_id

    def save(self, *args, **kwargs):
        value = (
            self.player.name
            + "-"
            + self.season
            + "-"
            + self.rarity.name
            + "-"
            + str(self.index)
        )
        if not self.slug:
            self.slug = slugify(value, allow_unicode=False)
        return super().save(*args, **kwargs)


class PlayerCardLike(models.Model):
    playercard = models.ForeignKey(
        PlayerCard, on_delete=models.CASCADE, related_name="likes"
    )
    user_id = models.IntegerField()

    class Meta:
        unique_together = ("playercard", "user_id")

    def __str__(self):
        return f"{self.playercard} - {self.user_id}"


class Bundle(models.Model):
    name = models.CharField(max_length=100)
    rarity = models.ForeignKey(CardRarity, on_delete=models.CASCADE)
    cards = models.ManyToManyField(
        PlayerCard, through="BundleCard", limit_choices_to={"owner_id": None}
    )
    cover_image = models.ImageField(upload_to="bundle_covers/", null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(null=True, blank=True)
    buyer_id = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_price(self):
        return self.price

    def mark_as_sold(self, buyer):
        self.sold_to = buyer
        self.is_available = False
        self.is_sold = True
        self.date_sold = timezone.now()
        self.save()

    @property
    def get_cards_in_bundle(self):
        return self.cards.all()


class BundleCard(models.Model):
    card_bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    player_card = models.ForeignKey(PlayerCard, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.player_card} in {self.card_bundle}"

    class Meta:
        unique_together = ["card_bundle", "player_card"]


class TeamCollection(models.Model):
    name=models.CharField(max_length=100)
    rarity_name = models.CharField(max_length=100)
    description=models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    cards = models.ManyToManyField(PlayerCard, blank=True)
    reward_id = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('collection:detail', kwargs={'pk': self.pk})
    
    def get_cards(self):
        return self.cards.all()
    
    
class CompletedCollection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    collection = models.ForeignKey(TeamCollection, on_delete=models.CASCADE)
    reward_id = models.IntegerField()
    reward_received = models.BooleanField(default=False)
    date_completed = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.collection}'
    
    class Meta:
        unique_together = ('user_id', 'collection')