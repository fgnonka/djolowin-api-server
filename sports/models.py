from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django_countries.fields import CountryField

SPORTS = [
    ("football", "Football"),
    ("basketball", "Basketball"),
]

class League(models.Model):
    name = models.CharField(_("League Name"), max_length=255)
    sport = models.CharField(_("Sport"), max_length=255, choices=SPORTS, default="football")
    country = CountryField(null=True, blank=True)
    year = models.IntegerField(_("Year"), default=2023)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "League"
        verbose_name_plural = "Leagues"

    def __str__(self):
        return self.name
    
    def _generate_slug(self):
        value = f"{self.name}-{self.country}"
        return slugify(value, allow_unicode=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_slug()
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse(f"{self.sport}:league-detail", kwargs={"slug": self.slug})


class Team(models.Model):
    name = models.CharField(_("Team Name"), max_length=255, null=True, blank=True)
    logo = models.ImageField(
        _("Team Logo"), upload_to="team_logos", null=True, blank=True
    )
    country = CountryField(null=True, blank=True)
    year = models.IntegerField(_("Year"))
    league = models.ForeignKey(
        League, on_delete=models.PROTECT, null=False, blank=False
    )
    sport = models.CharField(_("Sport"), max_length=255, choices=SPORTS, default="football")
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)

    class Meta:
        ordering = ["year"]
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        

    def __str__(self):
        return f"{self.name}---{self.league}"

    @property
    def get_country_display(self):
        return self.country.country.name
    
    @property
    def get_name(self):
        return f"{self.name} {self.year}"

    def _generate_slug(self):
        value = f"{self.name}-{self.year}"
        return slugify(value, allow_unicode=False)

    def get_absolute_url(self):
        return reverse("team:team-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_slug()
        return super().save(*args, **kwargs)


class Player(models.Model):
    POSITION_CHOICES = (
        ("GK", "Goalkeeper"),
        ("DEF", "Defender"),
        ("MID", "Midfielder"),
        ("FW", "Forward"),
    )
    name = models.CharField(_("Player Name"), max_length=255)
    position = models.CharField(_("Position"), max_length=3, choices=POSITION_CHOICES)
    date_of_birth = models.DateField(_("Date of Birth"))
    nationality = CountryField()
    jersey_number = models.PositiveIntegerField(_("Jersey Number"))
    picture = models.ImageField(upload_to="player_pictures", null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True)
    slug = models.SlugField(
        max_length=155,
        help_text="Label for URL configuration",
        null=True,
        blank=True,
        unique=True,
    )
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return f"{self.name} --- {self.position} --- {self.team}"

    @staticmethod
    def get_all_players():
        return Player.objects.all()

    @staticmethod
    def get_all_players_by_team(team):
        if team:
            return Player.objects.filter(team=team)
        else:
            return Player.objects.all()

    @property
    def get_player_age(self):
        team_year = self.team.year
        player_age = team_year - self.date_of_birth.year
        return player_age

    @property
    def get_player_position_verbose(self):
        return dict(Player.POSITION_CHOICES)[self.position]

    def _generate_slug(self):
        value = f"{self.name}-{self.team.country.country.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_slug()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("team:player-detail", kwargs={"slug": self.slug})
