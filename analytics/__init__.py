class CustomerEvents:
    """The different customer event types."""

    # Account related events
    ACCESS_TOKEN_GENERATED = "access_token_generated"
    ACCESS_TOKEN_INVALIDATED = "access_token_invalidated"
    ACCESS_TOKEN_EXPIRED = "access_token_expired"
    REFRESH_TOKEN_GENERATED = "refresh_token_generated"
    REFRESH_TOKEN_EXPIRED = "refresh_token_expired"

    SIGNUP_ATTEMPT = "signup_attempt"
    SIGNUP_ATTEMPT_FAILED = "signup_attempt_failed"
    SIGNUP_ATTEMPT_SUCCESSFUL = "signup_attempt_successful"
    ADMIN_ACCOUNT_CREATED = "admin_account_created"
    ADMIN_ACCOUNT_VERIFIED = "admin_account_verified"
    ACCOUNT_CREATED = "account_created"
    ACCOUNT_VERIFIED = "account_verified"
    ACCOUNT_DEACTIVATED = "account_deactivated"
    ACCOUNT_REACTIVATED = "account_reactivated"
    ACCOUNT_SUSPENDED = "account_suspended"

    ACCOUNT_LINKED_TO_GOOGLE = "account_linked_to_google"

    EMAIL_CHANGE_REQUEST = "email_change_request"
    EMAIL_CHANGED_BY_USER = "email_changed_by_user"
    USER_EMAIL_CHANGED_BY_ADMIN = "email_changed_by_admin"

    PASSWORD_RESET_REQUEST = "password_reset_request"
    PASSWORD_RESET_LINK_SENT = "password_reset_link_sent"
    PASSWORD_RESET_BY_USER = "password_reset_by_user"
    PASSWORD_CHANGED = "password_changed"

    PHONE_CHANGE_REQUEST = "phone_change_request"
    PHONE_CHANGED_BY_USER = "phone_changed_by_user"
    USER_PHONE_CHANGED_BY_ADMIN = "user_phone_changed_by_admin"

    FAILED_LOGIN_ATTEMPT = "failed_login_attempt"
    LOGIN_ATTEMPT = "login_attempt"
    SUCCESSFUL_LOGIN = "successful_login"
    SUCCESFULL_LOGOUT = "succesfull_logout"

    TWO_FACTOR_ENABLED = "two_factor_enabled"
    TWO_FACTOR_DISABLED = "two_factor_disabled"
    TWO_FACTOR_CODE_SENT = "two_factor_code_sent"
    TWO_FACTOR_CODE_RESENT = "two_factor_code_resent"
    TWO_FACTOR_FAILED = "two_factor_failed"
    TWO_FACTOR_SUCCESS = "two_factor_success"

    VERIFICATION_EMAIL_REQUESTED = "verification_email_requested"
    VERIFICATION_EMAIL_SENT = "verification_email_sent"

    CHOICES = [
        (ACCESS_TOKEN_GENERATED, "Access token generated"),
        (ACCESS_TOKEN_INVALIDATED, "Access token invalidated"),
        (ACCESS_TOKEN_EXPIRED, "Access token expired"),
        (REFRESH_TOKEN_GENERATED, "Refresh token generated"),
        (REFRESH_TOKEN_EXPIRED, "Refresh token expired"),
        (SIGNUP_ATTEMPT, "Signup attempt"),
        (SIGNUP_ATTEMPT_FAILED, "Signup attempt failed"),
        (SIGNUP_ATTEMPT_SUCCESSFUL, "Signup attempt successful"),
        (ACCOUNT_CREATED, "Account created"),
        (ADMIN_ACCOUNT_CREATED, "Admin account created"),
        (ACCOUNT_VERIFIED, "Account verified"),
        (ADMIN_ACCOUNT_VERIFIED, "Admin account verified"),
        (ACCOUNT_DEACTIVATED, "Account deactivated"),
        (ACCOUNT_REACTIVATED, "Account reactivated"),
        (ACCOUNT_SUSPENDED, "Account suspended"),
        (ACCOUNT_LINKED_TO_GOOGLE, "Account linked to Google"),
        (EMAIL_CHANGE_REQUEST, "Email change requested"),
        (EMAIL_CHANGED_BY_USER, "Email changed by user"),
        (USER_EMAIL_CHANGED_BY_ADMIN, "User email changed by admin"),
        (PASSWORD_RESET_REQUEST, "Password reset request"),
        (PASSWORD_RESET_LINK_SENT, "Password reset link sent"),
        (PASSWORD_RESET_BY_USER, "Password reset by user"),
        (PASSWORD_CHANGED, "Password changed"),
        (PHONE_CHANGE_REQUEST, "Phone change requested"),
        (PHONE_CHANGED_BY_USER, "Phone changed by user"),
        (USER_PHONE_CHANGED_BY_ADMIN, "User phone changed by admin"),
        (LOGIN_ATTEMPT, "Login attempt"),
        (FAILED_LOGIN_ATTEMPT, "Failed login attempt"),
        (SUCCESSFUL_LOGIN, "Successful login"),
        (SUCCESFULL_LOGOUT, "Succesfull logout"),
        (TWO_FACTOR_ENABLED, "Two factor enabled"),
        (TWO_FACTOR_DISABLED, "Two factor disabled"),
        (TWO_FACTOR_CODE_SENT, "Two factor code sent"),
        (TWO_FACTOR_CODE_RESENT, "Two factor code resent"),
        (TWO_FACTOR_FAILED, "Two factor failed"),
        (TWO_FACTOR_SUCCESS, "Two factor success"),
        (VERIFICATION_EMAIL_REQUESTED, "Verification email requested"),
        (VERIFICATION_EMAIL_SENT, "Verification email sent"),
    ]


class AuctionEvents:
    """The different auction event types."""

    AUCTION_CREATED = "auction_created"
    AUCTION_ENDED = "auction_ended"
    AUCTION_CANCELLED = "auction_cancelled"

    AUCTION_BID_PLACED = "bid_placed"

    AUCTION_REPORTED = "auction_reported"

    AUCTION_FOLLOWED = "auction_followed"
    AUCTION_UNFOLLOWED = "auction_unfollowed"

    AUCTION_SOLD = "auction_sold"
    AUCTION_NOT_SOLD = "auction_not_sold"

    CHOICES = [
        (AUCTION_CREATED, "Auction created"),
        (AUCTION_ENDED, "Auction ended"),
        (AUCTION_CANCELLED, "Auction cancelled"),
        (AUCTION_BID_PLACED, "Bid placed"),
        (AUCTION_REPORTED, "Auction reported"),
        (AUCTION_FOLLOWED, "Auction followed"),
        (AUCTION_UNFOLLOWED, "Auction unfollowed"),
        (AUCTION_SOLD, "Auction sold"),
        (AUCTION_NOT_SOLD, "Auction not sold"),
    ]


class InAppCurrencyEvents:
    """The different app currency event types."""

    IN_APP_CURRENCY_PURCHASED = "in_app_currency_purchased"
    IN_APP_CURRENCY_PURCHASE_FAILED = "in_app_currency_purchase_failed"
    IN_APP_CURRENCY_PURCHASE_REFUNDED = "in_app_currency_purchase_refunded"
    IN_APP_CURRENCY_PURCHASE_REVERSED = "in_app_currency_purchase_reversed"
    IN_APP_CURRENCY_PURCHASE_REVERSAL_FAILED = (
        "in_app_currency_purchase_reversal_failed"
    )

    CHOICES = [
        (IN_APP_CURRENCY_PURCHASED, "In app currency purchased"),
        (IN_APP_CURRENCY_PURCHASE_FAILED, "In app currency purchase failed"),
        (IN_APP_CURRENCY_PURCHASE_REFUNDED, "In app currency purchase refunded"),
        (IN_APP_CURRENCY_PURCHASE_REVERSED, "In app currency purchase reversed"),
        (
            IN_APP_CURRENCY_PURCHASE_REVERSAL_FAILED,
            "In app currency purchase reversal failed",
        ),
    ]


class CardEvents:
    """The different card event types."""

    CARD_PURCHASED = "card_purchased"
    CARD_PURCHASE_FAILED = "card_purchase_failed"

    CARD_SOLD = "card_sold"
    CARD_SALE_FAILED = "card_sale_failed"

    CARD_PRICE_UPDATED = "card_price_updated"
    CARD_PRICE_UPDATE_FAILED = "card_price_update_failed"
    CARD_MARKED_FOR_SALE = "card_marked_for_sale"
    CARD_MARKED_FOR_SALE_FAILED = "card_marked_for_sale_failed"
    CARD_UNMARKED_FOR_SALE = "card_unmarked_for_sale"
    CARD_UNMARKED_FOR_SALE_FAILED = "card_unmarked_for_sale_failed"

    CARD_LOCKED = "card_locked"
    CARD_UNLOCKED = "card_unlocked"

    CHOICES = [
        (CARD_PURCHASED, "Card purchased"),
        (CARD_PURCHASE_FAILED, "Card purchase failed"),
        (CARD_SOLD, "Card sold"),
        (CARD_SALE_FAILED, "Card sale failed"),
        (CARD_PRICE_UPDATED, "Card price updated"),
        (CARD_PRICE_UPDATE_FAILED, "Card price update failed"),
        (CARD_MARKED_FOR_SALE, "Card marked for sale"),
        (CARD_MARKED_FOR_SALE_FAILED, "Card marked for sale failed"),
        (CARD_UNMARKED_FOR_SALE, "Card unmarked for sale"),
        (CARD_UNMARKED_FOR_SALE_FAILED, "Card unmarked for sale failed"),
        (CARD_LOCKED, "Card locked"),
        (CARD_UNLOCKED, "Card unlocked"),
    ]
