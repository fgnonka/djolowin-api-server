from typing import Optional

from .models import CustomerEvent
from . import CustomerEvents


def access_token_generated_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCESS_TOKEN_GENERATED,
        payload=payload,
    )


def access_token_invalidated_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCESS_TOKEN_INVALIDATED,
        payload=payload,
    )


def access_token_expired_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCESS_TOKEN_EXPIRED,
        payload=payload,
    )


def refresh_token_generated_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.REFRESH_TOKEN_GENERATED,
        payload=payload,
    )


def refresh_token_expired_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.REFRESH_TOKEN_EXPIRED,
        payload=payload,
    )

def signup_attempt_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        event_type= CustomerEvents.SIGNUP_ATTEMPT,
        payload=payload,
    )

def signup_attempt_failed_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        event_type= CustomerEvents.SIGNUP_ATTEMPT_FAILED,
        payload=payload,
    )

def account_created_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_CREATED,
        payload=payload,
    )


def account_verified_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_VERIFIED,
        payload=payload,
    )


def account_deactivated_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_DEACTIVATED,
        payload=payload,
    )


def account_reactivated_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_REACTIVATED,
        payload=payload,
    )


def account_suspended_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_SUSPENDED,
        payload=payload,
    )


def admin_account_created_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ADMIN_ACCOUNT_CREATED,
        payload=payload,
    )


def admin_account_verified_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ADMIN_ACCOUNT_VERIFIED,
        payload=payload,
    )


def account_linked_to_google_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_LINKED_TO_GOOGLE,
        payload=payload,
    )


def account_linked_to_facebook_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_LINKED_TO_FACEBOOK,
        payload=payload,
    )


def account_linked_to_twitter_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.ACCOUNT_LINKED_TO_TWITTER,
        payload=payload,
    )


def email_change_request_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.EMAIL_CHANGE_REQUEST,
        payload=payload,
    )


def email_changed_by_user_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.EMAIL_CHANGED_BY_USER,
        payload=payload,
    )


def user_email_changed_by_admin_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.USER_EMAIL_CHANGED_BY_ADMIN,
        payload=payload,
    )


def password_reset_link_sent_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.PASSWORD_RESET_LINK_SENT,
        payload=payload,
    )


def password_reset_by_user_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.PASSWORD_RESET_BY_USER,
        payload=payload,
    )


def password_changed_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.PASSWORD_CHANGED,
        payload=payload,
    )


def phone_change_request_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.PHONE_CHANGE_REQUEST,
        payload=payload,
    )


def phone_changed_by_user_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.PHONE_CHANGED_BY_USER,
        payload=payload,
    )


def user_phone_changed_by_admin_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.USER_PHONE_CHANGED_BY_ADMIN,
        payload=payload,
    )

def login_attempt_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        event_type=CustomerEvents.LOGIN_ATTEMPT,
        payload=payload,
    )


def failed_login_attempt_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.FAILED_LOGIN_ATTEMPT,
        payload=payload,
    )


def successful_login_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.SUCCESSFUL_LOGIN,
        payload=payload,
    )


def successful_logout_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.SUCCESFULL_LOGOUT,
        payload=payload,
    )


def two_factor_enabled_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.TWO_FACTOR_ENABLED,
        payload=payload,
    )


def two_factor_disabled_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.TWO_FACTOR_DISABLED,
        payload=payload,
    )


def two_factor_code_sent_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.TWO_FACTOR_CODE_SENT,
        payload=payload,
    )


def two_factor_code_resent_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.TWO_FACTOR_CODE_RESENT,
        payload=payload,
    )


def two_factor_code_expired_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.TWO_FACTOR_CODE_EXPIRED,
        payload=payload,
    )


def two_factor_failed_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.TWO_FACTOR_FAILED,
        payload=payload,
    )


def two_factor_success_event(*, user_id: int, payload: Optional[dict] = None) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.TWO_FACTOR_SUCCESS,
        payload=payload,
    )


def verification_email_requested_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.VERIFICATION_EMAIL_REQUESTED,
        payload=payload,
    )


def verification_email_sent_event(
    *, user_id: int, payload: Optional[dict] = None
) -> None:
    CustomerEvent.objects.create(
        user_id=user_id,
        event_type=CustomerEvents.VERIFICATION_EMAIL_SENT,
        payload=payload,
    )
