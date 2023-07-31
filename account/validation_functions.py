import re
from django.contrib.auth import get_user_model
from .password.password_validation import get_default_password_validators
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status, serializers

from . import tasks
from .password.password_common import is_common_password, is_regex_validated
from .validators import (
    DEFAULT_RESERVED_NAMES,
    validate_confusables,
    validate_confusables_email,
)
from . import tasks

User = get_user_model()


# We are running the request parameter because the function will be called at the request level
def validate_credentials_at_registration(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password1")
    if email and username and password:
        validate_email_at_creation(email)
        validate_username_at_creation(username)
        validate_password_at_creation(password)
        check_similarities(username, email, password)
    else:
        tasks.signup_attempt_failed_event(
            payload={
                "ip_address": request.META.get("REMOTE_ADDR"),
                "message": "Incorrect credentials",
                "username": username,
                "email": email,
                "status": status.HTTP_400_BAD_REQUEST,
            }
        )
        raise serializers.ValidationError(_("Missing credentials. Try again."))
    return True


def check_similarities(username, email, password):
    """This method is used to check if the username,
    email and password are similar."""
    if username == password:
        raise serializers.ValidationError(_("Username and password must be different."))
    if email.split("@")[0] == password:
        raise serializers.ValidationError(_("Password and email must be different."))
    if username in password:
        raise serializers.ValidationError(
            _("Password cannot contain username. Modify your password.")
        )
    return True


def validate_username_at_creation(username: str):
    """This method is used to validate the username field."""
    check_username_length(username)
    check_username_not_in_reserved_names(username)
    check_username_does_not_exist(username)
    validate_confusables(username)
    return True


def validate_email_at_creation(email):
    """This method is used to validate the email field."""
    check_capital_letters(email)
    if User.objects.filter(email__iexact=email).exists():
        raise serializers.ValidationError(_("Email already exists."))
    if email.split("@")[0] in DEFAULT_RESERVED_NAMES:
        raise serializers.ValidationError(_("Email cannot be a reserved name."))
    return True


def validate_password_at_creation(password, User=None, password_validators=None):
    """This method is used to validate the password field."""
    if password:
        if re.search(r"\s", password):
            raise serializers.ValidationError(_("Password cannot contain spaces."))
        if password.isdigit():
            raise serializers.ValidationError(
                _("This password is entirely numeric."),
                code="password_entirely_numeric",
            )
        if len(password) < 8:
            raise serializers.ValidationError(
                _("Password must be at least 8 characters long.")
            )
        if is_common_password(password):
            raise serializers.ValidationError(_("This password is too common."))
        if not is_regex_validated(password):
            # We actually mean to say "If the password is not regex validated,
            # then we raise an error."
            raise serializers.ValidationError(
                _(
                    "Password must contain at least one number, one uppercase letter, one lowercase letter and one special character."
                )
            )
        validate_password(password, user=User)
        return True


def check_capital_letters(email):
    """This method is used to check if the email contains capital letters."""
    for letter in email:
        if letter.isupper():
            raise serializers.ValidationError(
                _("Email cannot contain capital letters.")
            )


def check_username_length(username):
    """This method is used to check the length of the username."""
    if username:
        if len(username) < 3 or len(username) > 50:
            raise serializers.ValidationError(
                _(
                    "Username must be at least 3 characters long and at most 50 characters."
                )
            )
    return True


def check_username_not_in_reserved_names(username):
    """This method is used to check if the username is in the DEFAULT_RESERVED_NAMES."""
    if username in DEFAULT_RESERVED_NAMES:
        raise serializers.ValidationError(
            _("Username cannot be in the reserved names.")
        )
    return True


def check_username_does_not_exist(username):
    """This method is used to check if the username exists."""
    if User.objects.filter(username__iexact=username).exists():
        raise serializers.ValidationError(_("Username already exists."))
    return True


def validate_password(password, user=None, password_validators=None):
    """
    Validate that the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except serializers.ValidationError as error:
            errors.append(error)
    if errors:
        return serializers.ValidationError(errors)
