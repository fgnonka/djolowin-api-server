from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from . import tasks
from . models import CustomUser as User

def handle_failed_login(email, ip_address):
    tasks.failed_login_attempt_event(
        payload={
            "ip_address": ip_address,
            "email": email,
            "status": str(status.HTTP_400_BAD_REQUEST),
        }
    )

def check_user_authentication(email, user, ip_address):
    filtered_user_by_email = User.objects.filter(email=email)

    if (
        filtered_user_by_email.exists()
        and filtered_user_by_email[0].auth_provider != "email"
    ):
        raise AuthenticationFailed(
            detail="Please continue your login using "
            + filtered_user_by_email[0].auth_provider
        )

    if not user:
        handle_failed_login(email, ip_address)
        raise AuthenticationFailed("Invalid credentials, try again")

    if not user.is_active:
        handle_failed_login(email, ip_address)
        raise AuthenticationFailed("Account disabled, contact admin")

    if not user.is_verified:
        handle_failed_login(email, ip_address)
        raise AuthenticationFailed("Your account is not verified.\n\n Please check your mailbox for the verification email")

