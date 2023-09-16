from functools import partial
from uuid import uuid4

from django.core.mail import send_mail
from django.db.models import JSONField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField, Country
from PIL import Image
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import ModelWithMetadata
from permission.models import PermissionsMixin, Permission
from .manager import CustomUserManager
from .validators import validate_possible_number
from . import CustomerEvents


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class Address(models.Model):
    """A model to represent a user's address."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user_address", on_delete=models.CASCADE, 
        null=True, blank=True
    )
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = CountryField(blank=True)
    postal_code = models.CharField(max_length=255, blank=True)

    

    def __str__(self):
        return f"{self.user.username}--{self.street_address}--{self.city}--{self.country}"

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.as_data == other.as_data

    class Meta:
        ordering = ("pk",)
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["street_address"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
            models.Index(fields=["country"]),
            models.Index(fields=["postal_code"]),
        ]

    def as_data(self):
        data = model_to_dict(self, exclude=["id", "user"])
        if isinstance(data["country"], Country):
            data["country"] = data["country"].code
        return data

    def get_copy(self):
        return Address.objects.create(**self.as_data())


AUTH_PROVIDERS = {
    "facebook": "facebook",
    "google": "google",
    "twitter": "twitter",
    "email": "email",
}


class CustomUser(PermissionsMixin, AbstractBaseUser, ModelWithMetadata):
    """Each `User` needs a human-readable unique identifier that we can use to
    represent the `User` in the UI. We want to index this column in the
    database to improve lookup performance"""

    username = models.CharField(
        _("username"),
        db_index=True,
        max_length=20,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("Last name"), max_length=50, blank=True, null=True)
    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(_("Email address"), unique=True)
    country = CountryField(_("Country"), blank=True)
    default_billing_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    date_of_birth = models.DateField(_("Date of birth"), blank=True, null=True)
    profile_img = models.ImageField(
        default="default.png", upload_to="profile_images", blank=True, null=True
    )
    phone_number = PossiblePhoneNumberField(blank=True, default="", db_index=True)
    login_points = models.PositiveIntegerField(default=0)
    # User Status
    # A timestamp representing when this object was created.
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("Last login"), blank=True, null=True)
    # A timestamp representing when this object was created.
    updated_at = models.DateTimeField(auto_now=True)
    verification_token = models.UUIDField(
        _("Account Verification Token"),
        default=uuid4,
        editable=False,
        null=True,
        blank=True,
    )
    verification_token_expiration = models.DateTimeField(
        _("Verification Token Expiration"), null=True, blank=True
    )
    reset_password_token = models.CharField(
        _("Password Token"), max_length=255, blank=True, null=True, default=""
    )
    reset_password_token_expiration = models.DateTimeField(
        _("Password Token Expiration"), null=True, blank=True
    )
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get("email")
    )
    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(_("Admin status"), default=False)
    # The 'is_superuser' flag is expected by Django to determine who can and
    # cannot access the admin site and perform all administrative actions.
    is_superuser = models.BooleanField(_("Superuser status"), default=False)
    # The `is_verified` flag is expected to determine if the user has verified his/her email address
    is_verified = models.BooleanField(_("Verified"), default=False)
    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(_("Active"), default=True)
    language_code = models.CharField(
        max_length=35, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )
    note = models.TextField(null=True, blank=True)
    search_document = models.TextField(blank=True, default="")
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = CustomUserManager()

    class Meta:
        ordering = ("email",)
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            models.Index(fields=["phone_number"]),
            models.Index(fields=["country"]),
        ]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effective_permissions = None

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.search_document = self.get_search_document()
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.profile_img.path)
        except FileNotFoundError:
            img = Image.open("media/default.png")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_img.path)
    
    @property
    def get_address_details(self):
        try:
            address = self.user_address
            
            return address.as_data()
        except Address.DoesNotExist:
            return None

    def get_absolute_url(self):
        """Return the URL to the user detail page."""
        return reverse("accounts:user-detail", kwargs={"uuid": self.uuid})

    def get_search_document(self):
        """Returns a string used for indexing this object in a search engine."""
        document = self.username
        if self.first_name:
            document += f" {self.first_name}"
        if self.last_name:
            document += f" {self.last_name}"
        if self.email:
            document += f" {self.email}"
        if self.phone_number:
            document += f" {self.phone_number}"
        if self.country:
            document += f" {self.country.name}"
        return document

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


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
    user = models.ForeignKey(
        CustomUser, related_name="events", on_delete=models.CASCADE, null=True
    )
    payload = JSONField(_("Event parameters"), blank=True, default=dict, null=True)

    class Meta:
        ordering = ("-date",)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(type={self.event_type!r}, user={self.user!r})"
        )

    def __str__(self):
        return f"{self.event_type} - {self.user} - {self.date.strftime('%-d %B %Y, %I:%M:%S%p')} - {self.initiator}"


class CheckInHistory(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="check_in_history", on_delete=models.CASCADE
    )
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_in_window = models.CharField(max_length=255, blank=True, null=True)


# ------------------- USER GROUP RELATED MODELS ------------------- #


class GroupManager(models.Manager):
    """The manager for the auth's Group model."""

    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Group(models.Model):
    """The system provides a way to group users.

    Groups are a generic way of categorizing users to apply permissions, or
    some other label, to those users. A user can belong to any number of
    groups.

    A user in a group automatically has all the permissions granted to that
    group. For example, if the group 'Site editors' has the permission
    can_edit_home_page, any user in that group will have that permission.

    Beyond permissions, groups are a convenient way to categorize users to
    apply some label, or extended functionality, to them. For example, you
    could create a group 'Special users', and you could write code that would
    do special things to those users -- such as giving them access to a
    members-only portion of your site, or sending them members-only email
    messages.
    """

    name = models.CharField("name", max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name="permissions",
        blank=True,
    )
    restricted_access_to_channels = models.BooleanField(default=False)

    objects = GroupManager()

    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


# ------------------- WALLET RELATED MODELS ------------------- #


class UserWallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    reserved_balance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_balance(self):
        return self.balance - self.reserved_balance

    @property
    def owner_name(self):
        return self.user.username

    def __str__(self):
        return f"Wallet of {self.user}"

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")


# ------------------- USER PREFENCES RELATED MODELS ------------------- #


class UserPreferences(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="preferences", on_delete=models.CASCADE
    )
    # A user can choose to receive marketing emails from us.
    receive_email_updates = models.BooleanField(default=True)
    # A user can choose to receive marketing text messages from us.
    receive_sms_updates = models.BooleanField(default=True)
    # A user can choose to receive marketing phone calls from us.
    receive_phone_call_updates = models.BooleanField(default=True)
    # A user can choose to receive marketing direct mail from us.
    receive_direct_mail_updates = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("User Preference")
        verbose_name_plural = _("User Preferences")

    def __str__(self):
        return f"Preference of {self.user}"
