class CustomerEvents:
    """The different customer event types."""

    # Account related events
    USER_SIGNUP = "user_signup"
    USER_ACCOUNT_VERIFIED = "user_account_verified"
    USER_LOGIN_ATTEMPT = "user_login_attempt"
    USER_LOGIN_FAILED = "user_login_failed"
    USER_LOGIN_SUCCESSFUL = "user_login_successful"
    USER_ACCOUNT_DEACTIVATED = "user_account_deactivated"
    PASSWORD_RESET_LINK_SENT = "password_reset_link_sent"
    PASSWORD_RESET = "password_reset"
    PASSWORD_CHANGED = "password_changed"
    EMAIL_CHANGE_REQUEST = "email_change_request"
    EMAIL_CHANGED = "email_changed"
    PHONE_CHANGE_REQUEST = "phone_change_request"
    PHONE_CHANGED = "phone_changed"
    VERIFICATION_EMAIL_SENT = "verification_email_sent"
    NEW_VERIFICATION_EMAIL_REQUESTED = "new_verification_email_requested"
    NEW_VERIFICATION_EMAIL_SENT = "new_verification_email_sent"

    # Trade related events
    PLACED_SINGLE_ORDER = "placed_single_order"  # created a single item order
    PLACED_BUNDLE_ORDER = "placed_bundle_order"  # created a bundles items order
    PLACED_TOPUP_ORDER = "placed_topup_order"  # created a topup order
    CURRENCY_WITHDRAWAL = (
        "currency_withdrawal"  # currency withdrawn from availabe balance
    )
    CURRENCY_DEPOSIT = "currency_deposit"  # currency deposited on account

    # Promotion related events
    WATCHED_ADS_IN_PLATFORM = "watched_ads_in_platform"  # watched ads
    USED_PROMO_CODE = "used_promo_code"  # used a promo code

    # Staff actions over customers events
    CUSTOMER_DELETED = "customer_deleted"  # staff user deleted a customer
    EMAIL_ASSIGNED = "email_assigned"  # the staff user assigned a email to the customer
    NAME_ASSIGNED = "name_assigned"  # the staff user added set a name to the customer
    NOTE_ADDED_TO_ORDER = "note_added_to_order"  # the staff user added a note to the customer

    CHOICES = [
        # Account Maintenance
        (USER_SIGNUP, "The user signed up"),
        (USER_ACCOUNT_VERIFIED, "The user account was verified"),
        (USER_LOGIN_ATTEMPT, "The user attempted to login"),
        (USER_LOGIN_FAILED, "The user login failed"),
        (USER_LOGIN_SUCCESSFUL, "The user login was successful"),
        (USER_ACCOUNT_DEACTIVATED, "The user account was deactivated"),
        (PASSWORD_RESET_LINK_SENT, "Password reset link was sent to the customer"),
        (PASSWORD_RESET, "The account password was reset"),
        (PASSWORD_CHANGED, "The account password was changed"),
        (
            PHONE_CHANGE_REQUEST,
            "The user requested to change the account's phone number.",
        ),
        (PHONE_CHANGED, "The account phone number was changed"),
        (
            EMAIL_CHANGE_REQUEST,
            "The user requested to change the account's email address.",
        ),
        (EMAIL_CHANGED, "The account email address was changed"),
        (VERIFICATION_EMAIL_SENT, "A verification email was sent to the customer"),
        (NEW_VERIFICATION_EMAIL_REQUESTED, "A new verification email was requested"),
        (NEW_VERIFICATION_EMAIL_SENT, "A new verification email was sent"),
        (CUSTOMER_DELETED, "A customer was deleted"),
        (NAME_ASSIGNED, "A customer's name was edited"),
        (EMAIL_ASSIGNED, "A customer's email address was edited"),
        (NOTE_ADDED_TO_ORDER, "A note was added to the customer order"),
        # Account activity
        (CURRENCY_WITHDRAWAL, "The customer withdrew some currency"),
        (CURRENCY_DEPOSIT, "The customer deposited some currency"),
        (PLACED_SINGLE_ORDER, "A single order was placed"),
        (PLACED_BUNDLE_ORDER, "A bundled order was placed"),
        (PLACED_TOPUP_ORDER, "A topup order was placed"),
        # Promotions
        (WATCHED_ADS_IN_PLATFORM, "The customer watched ads in the platform"),
        (USED_PROMO_CODE, "The customer used a promo code"),
    ]
