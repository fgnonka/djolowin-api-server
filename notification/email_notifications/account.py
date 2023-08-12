class AccountRelatedEmailTypes:
    """The different types of Account Related Emails that can be sent to a user."""
    
    ACCOUNT_ACTIVATION_CONFIRMATION_EMAIL = "account_activation_confirmation_email"
    ACCOUNT_DEACTIVATION_EMAIL = "account_deactivation_email"
    ACCOUNT_REGISTRATION_EMAIL = "account_registration_email"
    ACCOUNT_SUSPENDED_EMAIL = "account_suspended_email"
    ACCOUNT_SECURITY_ALERT_EMAIL = "account_security_alert_email"
    ACCOUNT_TERMINATION_EMAIL = "account_termination_email"
    EMAIL_ADDRESS_CHANGE_REQUEST_EMAIL = "email_address_change_request_email"
    EMAIL_ADDRESS_VERIFICATION_REMINDER_EMAIL = "email_address_verification_reminder_email"
    PASSWORD_RESET_REQUEST_EMAIL = "password_reset_request_email"
    PASSWORD_RESET_CONFIRMATION_EMAIL = "password_reset_confirmation_email"
    WELCOME_EMAIL = "welcome_email"
    
    CHOICES = [
        (ACCOUNT_ACTIVATION_CONFIRMATION_EMAIL, "Account activation confirmation email"),
        (ACCOUNT_DEACTIVATION_EMAIL, "Account deactivation email"),
        (ACCOUNT_REGISTRATION_EMAIL, "Account registration email"),
        (ACCOUNT_SECURITY_ALERT_EMAIL, "Account security alert email"),
        (ACCOUNT_TERMINATION_EMAIL, "Account termination email"),
        (EMAIL_ADDRESS_CHANGE_REQUEST_EMAIL, "Email address change request email"),
        (EMAIL_ADDRESS_VERIFICATION_REMINDER_EMAIL, "Email address verification reminder email"),
        (PASSWORD_RESET_REQUEST_EMAIL, "Password reset request email"),
        (PASSWORD_RESET_CONFIRMATION_EMAIL, "Password reset confirmation email"),
        (WELCOME_EMAIL, "Welcome email"),
    ]