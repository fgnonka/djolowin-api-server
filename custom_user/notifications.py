from typing import Optional
from urllib.parse import urlencode

from django.contrib.auth.tokens import default_token_generator

from core.notification.utils import get_site_context
from core.notify_events import NotifyEventType
from core.tokens import account_delete_token_generator
from core.utils.url import prepare_url

from .models import CustomUser


def get_default_payload(user: CustomUser) -> dict:
    """Returns the default payload for events"""
    payload = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "private_metadata": user.private_metadata,
        "metadata": user.metadata,
        "language_code": user.language_code,
    }
    return payload


def get_user_custom_payload(user: CustomUser) -> dict:
    """Returns the custom payload for events"""
    payload = {
        "user": get_default_payload(user),
        "reciplent_email": user.email,
        **get_site_context(),
    }
    return payload


def send_password_reset_notification(
    redirect_url: str,
    user: CustomUser,
    manager,
    channel_slug: Optional[str],
    staff=False,
):
    """Trigger sending a password reset notification for the given user/staff."""
    token = default_token_generator.make_token(user)
    params = urlencode({"email": user.email, "token": token})
    reset_url = prepare_url(redirect_url, params)

    payload = {
        "user": get_default_payload(user),
        "recipient_email": user.email,
        "token": token,
        "reset_url": reset_url,
        "channel_slug": channel_slug,
        **get_site_context(),
    }

    event = (
        NotifyEventType.ACCOUNT_STAFF_PASSWORD_RESET
        if staff
        else NotifyEventType.ACCOUNT_PASSWORD_RESET
    )
    manager.notify(event, payload, channel_slug=channel_slug)


def send_account_confirmation(
    user: CustomUser, manager, redirect_url: str, channel_slug: Optional[str]
):
    """Trigger sending an account confirmation notification for the given user."""
    token = default_token_generator.make_token(user)
    params = urlencode({"email": user.email, "token": token})
    confirmation_url = prepare_url(redirect_url, params)

    payload = {
        "user": get_default_payload(user),
        "recipient_email": user.email,
        "token": token,
        "confirmation_url": confirmation_url,
        "channel_slug": channel_slug,
        **get_site_context(),
    }
    manager.notify(
        NotifyEventType.ACCOUNT_CONFIRMATION, payload, channel_slug=channel_slug
    )


def send_request_user_change_email_notification(
    user: CustomUser, manager, redirect_url: str, channel_slug: Optional[str]
):
    """Trigger sending an request user change email notification for the given user."""
    token = default_token_generator.make_token(user)
    params = urlencode({"email": user.email, "token": token})
    confirmation_url = prepare_url(redirect_url, params)

    payload = {
        "user": get_default_payload(user),
        "recipient_email": user.email,
        "token": token,
        "confirmation_url": confirmation_url,
        "channel_slug": channel_slug,
        **get_site_context(),
    }
    manager.notify(
        NotifyEventType.ACCOUNT_CHANGE_EMAIL_REQUEST, payload, channel_slug=channel_slug
    )


def send_user_change_email_notification(
    recipient_email, user: CustomUser, manager, channel_slug
):
    """ "Trigger sending an user change email notification for the given user."""
    payload = {
        "user": get_default_payload(user),
        "recipient_email": recipient_email,
        "channel_slug": channel_slug,
        "old_email": user.email,
        "new_email": recipient_email,
        **get_site_context(),
    }
    manager.notify(
        NotifyEventType.ACCOUNT_CHANGE_EMAIL_CONFIRMATION,
        payload,
        channel_slug=channel_slug,
    )


def send_user_delete_confirmaion_notification(
    user: CustomUser, manager, channel_slug, redirect_url
):
    token = account_delete_token_generator.make_token(user)
    params = urlencode({"token": token})
    delete_url = prepare_url(params, redirect_url)
    payload = {
        "user": get_default_payload(user),
        "recipient_email": user.email,
        "token": token,
        "delete_url": delete_url,
        "channel_slug": channel_slug,
        **get_site_context(),
    }
    manager.notify(
        NotifyEventType.ACCOUNT_DELETE_CONFIRMATION, payload, channel_slug=channel_slug
    )

def send_set_password_notification(
    user: CustomUser, manager, redirect_url: str, channel_slug: Optional[str], staff=False):
    """Trigger sending a set password notification for the given user/staff."""
    token = default_token_generator.make_token(user)
    params = urlencode({"email": user.email, "token": token})
    password_set_url = prepare_url(params, redirect_url)
    payload = {
        "user": get_default_payload(user),
        "recipient_email": user.email,
        "token": token,
        "password_set_url": password_set_url,
        "channel_slug": channel_slug,
        **get_site_context(),
    }
    if staff:
        event = NotifyEventType.ACCOUNT_STAFF_SET_PASSWORD
    else:
        event = NotifyEventType.ACCOUNT_SET_CUSTOMER_PASSWORD
    manager.notify(event, payload, channel_slug=channel_slug)