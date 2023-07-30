from typing import Optional

from . import CustomerEvents
from .models import CustomUser, CustomerEvent


def customer_user_signup_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "user registered" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.USER_SIGNUP,
        user=user,
    )


def customer_user_account_verified_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "user account verified" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.USER_ACCOUNT_VERIFIED,
        user=user,
    )


def customer_user_login_attempt_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "user login attempt" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.USER_LOGIN_ATTEMPT,
        user=user,
    )


def customer_user_login_failed_event(*,parameters) -> CustomerEvent:
    """Records the "user login failed" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.USER_LOGIN_FAILED,
        parameters=parameters,
    )


def customer_user_login_successful_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "user login successful" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.USER_LOGIN_SUCCESSFUL,
        user=user,
    )


def customer_account_deactivated_event(
    *, user: CustomUser, account_id: int
) -> CustomerEvent:
    """Records the "account deactivated" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.USER_ACCOUNT_DEACTIVATED,
        user=user,
        parameters={"account_id": account_id},
    )


def customer_password_reset_link_sent_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "password reset link sent" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.PASSWORD_RESET_LINK_SENT,
        user=user,
    )


def customer_password_reset_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "password reset" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.PASSWORD_RESET,
        user=user,
    )


def customer_password_changed_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "password changed" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.PASSWORD_CHANGED,
        user=user,
    )


def customer_email_change_request_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "email change request" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.EMAIL_CHANGE_REQUEST,
        user=user,
    )


def customer_email_changed_event(
    *, user: int, parameters: dict
) -> Optional[CustomerEvent]:
    return CustomerEvent.objects.create(
        user=user, type=CustomerEvents.EMAIL_CHANGED, parameters=parameters
    )


def customer_phone_change_request_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "phone change request" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.PHONE_CHANGE_REQUEST,
        user=user,
    )


def customer_phone_changed_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "phone changed" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.PHONE_CHANGED,
        user=user,
    )


def customer_verification_email_sent_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "verification email sent" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.VERIFICATION_EMAIL_SENT,
        user=user,
    )


def customer_new_verification_email_requested_event(
    *, user: CustomUser
) -> CustomerEvent:
    """Records the "new verification email requested" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.NEW_VERIFICATION_EMAIL_REQUESTED,
        user=user,
    )


def customer_new_verification_email_sent_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "new verification email sent" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.NEW_VERIFICATION_EMAIL_SENT,
        user=user,
    )


def customer_currency_withdrawal_event(
    *, user: CustomUser, amount: int
) -> CustomerEvent:
    """Records the "currency withdrawal" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.CURRENCY_WITHDRAWAL,
        user=user,
        parameters={"amount": amount},
    )


def customer_currency_deposit_event(*, user: CustomUser, amount: int) -> CustomerEvent:
    """Records the "currency deposit" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.CURRENCY_DEPOSIT,
        user=user,
        parameters={"amount": amount},
    )


def customer_watched_ads_event(*, user: CustomUser) -> CustomerEvent:
    """Records the "watched ads" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.WATCHED_ADS,
        user=user,
    )


def customer_used_promo_code_event(
    *, user: CustomUser, promo_code: str
) -> CustomerEvent:
    """Records the "used promo code" event for a given user."""
    return CustomerEvent.objects.create(
        event_type=CustomerEvents.USED_PROMO_CODE,
        user=user,
        parameters={"promo_code": promo_code},
    )


# def customer_placed_single_order_event(*, user: CustomUser, order: Order) -> Optional[CustomerEvent]:
#     return CustomerEvent.objects.create(
#         user=user, order=order, type=CustomerEvents.PLACED_SINGLE_ORDER
#     )

# def customer_placed_bundle_order_event(*, user: CustomUser, order: Order) -> Optional[CustomerEvent]:
#     return CustomerEvent.objects.create(
#         user=user, order=order, type=CustomerEvents.PLACED_BUNDLE_ORDER
#     )


# def customer_added_to_note_order_event(
#     *, user: Optional[CustomUser], order: Order, message: str
# ) -> CustomerEvent:
#     return CustomerEvent.objects.create(
#         user=user,
#         order=order,
#         type=CustomerEvents.NOTE_ADDED_TO_ORDER,
#         parameters={"message": message},
#     )


# def customer_downloaded_a_digital_link_event(
#     *, user: CustomUser, order_line: OrderLine
# ) -> CustomerEvent:
#     return CustomerEvent.objects.create(
#         user=user,
#         order=order_line.order,
#         type=CustomerEvents.DIGITAL_LINK_DOWNLOADED,
#         parameters={"order_line_pk": order_line.pk},
#     )


def customer_deleted_event(
    *, staff_user: Optional[CustomUser], deleted_count: int = 1
) -> CustomerEvent:
    return CustomerEvent.objects.create(
        user=staff_user,
        order=None,
        type=CustomerEvents.CUSTOMER_DELETED,
        parameters={"count": deleted_count},
    )


def assigned_email_to_a_customer_event(
    *, staff_user: Optional[CustomUser], new_email: str
) -> CustomerEvent:
    return CustomerEvent.objects.create(
        user=staff_user,
        order=None,
        type=CustomerEvents.EMAIL_ASSIGNED,
        parameters={"message": new_email},
    )


def assigned_name_to_a_customer_event(
    *, staff_user: Optional[CustomUser], new_name: str
) -> CustomerEvent:
    return CustomerEvent.objects.create(
        user=staff_user,
        order=None,
        type=CustomerEvents.NAME_ASSIGNED,
        parameters={"message": new_name},
    )
