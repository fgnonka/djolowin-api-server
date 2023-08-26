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
    ACCOUNT_LINKED_TO_FACEBOOK = "account_linked_to_facebook"
    ACCOUNT_LINKED_TO_TWITTER = "account_linked_to_twitter"
    
    EMAIL_CHANGE_REQUEST = "email_change_request"
    EMAIL_CHANGED_BY_USER = "email_changed_by_user"
    USER_EMAIL_CHANGED_BY_ADMIN = "email_changed_by_admin"
    
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
    TWO_FACTOR_CODE_EXPIRED = "two_factor_code_expired"
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
        (ACCOUNT_LINKED_TO_FACEBOOK, "Account linked to Facebook"),
        (ACCOUNT_LINKED_TO_TWITTER, "Account linked to Twitter"),
        
        (EMAIL_CHANGE_REQUEST, "Email change requested"),
        (EMAIL_CHANGED_BY_USER, "Email changed by user"),
        (USER_EMAIL_CHANGED_BY_ADMIN, "User email changed by admin"),
        
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
        (TWO_FACTOR_CODE_EXPIRED, "Two factor code expired"),
        (TWO_FACTOR_FAILED, "Two factor failed"),
        (TWO_FACTOR_SUCCESS, "Two factor success"),
        
        (VERIFICATION_EMAIL_REQUESTED, "Verification email requested"),
        (VERIFICATION_EMAIL_SENT, "Verification email sent"),
    ]