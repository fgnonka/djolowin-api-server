from celery import shared_task
from typing import Optional

from .models import CustomUser, CustomerEvent, UserWallet
from . import CustomerEvents


@shared_task
def access_token_generated_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(pk=user_id)
    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCESS_TOKEN_GENERATED,
        payload=payload,
    )
    return "access_token_generated_event"


@shared_task
def access_token_invalidated_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)
    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCESS_TOKEN_INVALIDATED,
        payload=payload,
    )


@shared_task
def access_token_expired_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCESS_TOKEN_EXPIRED,
        payload=payload,
    )


@shared_task
def refresh_token_generated_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.REFRESH_TOKEN_GENERATED,
        payload=payload,
    )


@shared_task
def refresh_token_expired_event(
    initiator=None, *, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        initiator=initiator,
        event_type=CustomerEvents.REFRESH_TOKEN_EXPIRED,
        payload=payload,
    )


@shared_task
def signup_attempt_event(initiator=None, *, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        initiator=initiator,
        event_type=CustomerEvents.SIGNUP_ATTEMPT,
        payload=payload,
    )


@shared_task
def signup_attempt_failed_event(
    initiator=None, *, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        initiator=initiator,
        event_type=CustomerEvents.SIGNUP_ATTEMPT_FAILED,
        payload=payload,
    )


@shared_task
def signup_attempt_successful_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(pk=user_id)
    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.SIGNUP_ATTEMPT_SUCCESSFUL,
        payload=payload,
    )


@shared_task
def account_created_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_CREATED,
        payload=payload,
    )


@shared_task
def account_verified_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_VERIFIED,
        payload=payload,
    )


@shared_task
def account_deactivated_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_DEACTIVATED,
        payload=payload,
    )


@shared_task
def account_reactivated_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_REACTIVATED,
        payload=payload,
    )


@shared_task
def account_suspended_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_SUSPENDED,
        payload=payload,
    )


@shared_task
def admin_account_created_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ADMIN_ACCOUNT_CREATED,
        payload=payload,
    )


@shared_task
def admin_account_verified_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ADMIN_ACCOUNT_VERIFIED,
        payload=payload,
    )


@shared_task
def account_linked_to_google_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_LINKED_TO_GOOGLE,
        payload=payload,
    )


@shared_task
def account_linked_to_facebook_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_LINKED_TO_FACEBOOK,
        payload=payload,
    )


@shared_task
def account_linked_to_twitter_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.ACCOUNT_LINKED_TO_TWITTER,
        payload=payload,
    )


@shared_task
def email_change_request_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.EMAIL_CHANGE_REQUEST,
        payload=payload,
    )


@shared_task
def email_changed_by_user_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.EMAIL_CHANGED_BY_USER,
        payload=payload,
    )


@shared_task
def user_email_changed_by_admin_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.USER_EMAIL_CHANGED_BY_ADMIN,
        payload=payload,
    )


@shared_task
def password_reset_by_user_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.PASSWORD_RESET_BY_USER,
        payload=payload,
    )


@shared_task
def password_changed_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.PASSWORD_CHANGED,
        payload=payload,
    )


@shared_task
def phone_change_request_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.PHONE_CHANGE_REQUEST,
        payload=payload,
    )


@shared_task
def phone_changed_by_user_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.PHONE_CHANGED_BY_USER,
        payload=payload,
    )


@shared_task
def user_phone_changed_by_admin_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.USER_PHONE_CHANGED_BY_ADMIN,
        payload=payload,
    )


@shared_task
def login_attempt_event(initiator=None, *, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        initiator=initiator,
        event_type=CustomerEvents.LOGIN_ATTEMPT,
        payload=payload,
    )


@shared_task
def failed_login_attempt_event(
    initiator=None, *, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        initiator=initiator,
        event_type=CustomerEvents.FAILED_LOGIN_ATTEMPT,
        payload=payload,
    )


@shared_task
def successful_login_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.SUCCESSFUL_LOGIN,
        payload=payload,
    )


@shared_task
def successful_logout_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.SUCCESSFUL_LOGOUT,
        payload=payload,
    )


@shared_task
def two_factor_enabled_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.TWO_FACTOR_ENABLED,
        payload=payload,
    )


@shared_task
def two_factor_disabled_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.TWO_FACTOR_DISABLED,
        payload=payload,
    )


def two_factor_code_sent_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.TWO_FACTOR_CODE_SENT,
        payload=payload,
    )


def two_factor_code_resent_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.TWO_FACTOR_CODE_RESENT,
        payload=payload,
    )


def two_factor_code_expired_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.TWO_FACTOR_CODE_EXPIRED,
        payload=payload,
    )


def two_factor_failed_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.TWO_FACTOR_FAILED,
        payload=payload,
    )


def two_factor_success_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.TWO_FACTOR_SUCCESS,
        payload=payload,
    )


@shared_task
def verification_email_requested_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.VERIFICATION_EMAIL_REQUESTED,
        payload=payload,
    )


@shared_task
def verification_email_sent_event(
    initiator=None, *, user_id: int, payload: Optional[dict] = None
) -> None:
    user = CustomUser.objects.get(id=user_id)

    CustomerEvent.objects.create(
        user=user,
        initiator=initiator,
        event_type=CustomerEvents.VERIFICATION_EMAIL_SENT,
        payload=payload,
    )


# --------------------------------------WALLETS RELATED TASKS--------------------------------------#


@shared_task
def transfer_coins_to_seller(auction_details):
    """This function is called when an auction ends.
    It has two tasks:
    1. Transfer the coins to the seller.
    2. Withdraw the coins from the winner's reserved balance.
    """
    seller_wallet = UserWallet.objects.get(user_id=auction_details["seller_id"])
    winner_wallet = UserWallet.objects.get(user_id=auction_details["highest_bidder"])
    winning_bid = auction_details["current_bid"]
    seller_wallet.balance += winning_bid
    winner_wallet.reserved_balance -= winning_bid
    seller_wallet.save()
    winner_wallet.save()
