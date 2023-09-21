from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import (
    get_user_model,
)

from django.shortcuts import redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView as RetrieveAPIView

from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from core.mixins import ClientIPMixin
from notification import tasks as notification_tasks

from .. import tasks
from .. import kafka_producers

from ..models import CustomUser as User
from ..renderers import UserRenderer
from ..serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from ..mixins import (
    TokenExpirationMixin,
    TokenVerificationMixin,
    # JWTAuthenticationFromCookieMixin,
)
from ..validation_functions import (
    validate_credentials_at_registration,
    validate_password,
)
from ..wallet_functions import create_wallet

User = get_user_model()

FRONTEND_URL = settings.DJOLOWIN_FRONTEND_URL


class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "User is authenticated", "user": request.user.email},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "User is not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LoginAPIView(APIView, ClientIPMixin):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email")
        ip_address = self.get_client_ip(request)
        tasks.login_attempt_event.delay(
            initiator=ip_address, payload={"ip_address": ip_address, "email": email}
        )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=email)

        tasks.successful_login_event.delay(
            user_id=user.id,
            initiator=email,
            payload={"ip_address": ip_address, "email": email},
        )
        # Kafka event "successful_login" is sent here
        kafka_producers.kafka_successful_login_event(user.id)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        tasks.successful_logout_event.delay(
            user_id=request.user.id,
            initiator=request.user.email,
            payload={
                "email": request.user.email,
                "ip_address": request.META.get("REMOTE_ADDR"),
            },
        )
        # Kafka event "successful_logout" is sent here
        kafka_producers.kafka_successful_logout_event(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ObtainNewAccessTokenView(
    APIView,
    TokenExpirationMixin,
    TokenVerificationMixin,
):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        if refresh_token_str is not None:
            try:
                if self.verify_refresh_token(refresh_token_str):
                    refresh_token = RefreshToken(refresh_token_str)
                    access_token = refresh_token.access_token
                    payload_user_id = access_token.payload.get("user_id")
                    expiration = self.get_token_expiration()
                    json_expiration = datetime.timestamp(expiration)
                    tasks.access_token_generated_event.delay(
                        user_id=payload_user_id, payload={"expiration": json_expiration}
                    )
                    response = Response(
                        {
                            "message": f"Access token refreshed {access_token} ",
                            "access_token": str(access_token),
                        },
                        status=status.HTTP_200_OK,
                    )
                    # Kafka event "access_token_generated" is sent here
                    kafka_producers.kafka_access_token_generated_event(payload_user_id)
                    return response
                else:
                    return Response(
                        {"message": "Invalid or expired refresh token"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except TokenError as e:
                return Response(
                    {"message": "Invalid or expired refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"message": "No refresh token in session. Please login again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class PasswordResetAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        reset_token = kwargs["token"]
        password = request.data.get("password2")
        if not password:
            return Response(
                {"message": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(reset_password_token=reset_token)
        except User.DoesNotExist:
            return Response(
                {"message": "An invalid token was submitted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the token has expired
        current_datetime = timezone.now()
        if (
            user.reset_password_token_expiration
            and current_datetime > user.reset_password_token_expiration
        ):
            return Response(
                {"message": "Reset token has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Reset the user's password and remove the reset token
        try:
            validate_password(password)
        except Exception as error:
            return Response(
                {"message": "Password is not valid", "error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(password)
        user.reset_password_token = None
        user.reset_password_token_expiration = None
        user.save()

        # Kafka event "password_reset_by_user" is sent here
        kafka_producers.kafka_password_reset_by_user_event(user.id)

        # Create an event log for the password reset
        tasks.password_reset_by_user_event.delay(
            user_id=user.id,
            initiator=user.email,
            payload={"email": user.email},
        )
        return Response(
            {"message": "Password reset successfully."}, status=status.HTTP_200_OK
        )


class PasswordResetRequestAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # Token expiration time in seconds (e.g., 1 hour)
        TOKEN_EXPIRATION_SECONDS = 3600

        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "No user found with this email address."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate a new password reset token
        reset_token = get_random_string(length=32)

        # Calculate the expiration timestamp
        expiration_datetime = timezone.now() + timedelta(
            seconds=TOKEN_EXPIRATION_SECONDS
        )

        # Save the reset token and timestamp in the user object
        user.reset_password_token = reset_token
        user.reset_password_token_expiration = expiration_datetime
        user.save()

        # Kafka event "password_reset_request" is sent here
        kafka_producers.kafka_password_reset_request_event(user.id)

        return Response(
            {"message": "Password reset link sent to your email."},
            status=status.HTTP_200_OK,
        )


class RequestEmailVerificationView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response(
                    {"message": "Email already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                tasks.verification_email_requested_event.delay(
                    user_id=user.id,
                    initiator=user.email,
                    payload={"email": user.email},
                )
                notification_tasks.send_verification_email.delay(
                    username=user.username,
                    email=user.email,
                    verification_link=f"{FRONTEND_URL}/verify-email/{user.verification_token}",
                )
                return Response(
                    {"message": "Verification email sent"},
                    status=status.HTTP_200_OK,
                )
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class SignupView(APIView, ClientIPMixin, TokenExpirationMixin):
    authentication_classes = []
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        ip_address = self.get_client_ip(request)
        user = request.data
        serializer = self.serializer_class(data=user)
        validate_credentials_at_registration(request)
        serializer.is_valid(raise_exception=True)

        form_email = serializer.validated_data["email"]
        tasks.signup_attempt_event.delay(
            initiator=ip_address,
            payload={"ip_address": ip_address, "email": form_email},
        )
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        try:
            wallet = create_wallet(user.id)
        except Exception as error:
            print(error)
        tasks.signup_attempt_successful_event.delay(
            user_id=user.id,
            initiator=user.email,
            payload={"ip_address": ip_address, "email": form_email},
        )
        # Kafka event "account_created" is sent here
        kafka_producers.kafka_user_account_created_event(user.id)
        return Response(
            user_data, status=status.HTTP_201_CREATED, content_type="application/json"
        )


class ValidateTokenView(APIView, TokenVerificationMixin, BlacklistMixin):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token or not refresh_token:
            return Response(
                {"message": "No token provided, please login"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if self.verify_access_token(access_token):
            return Response(
                {"message": "Valid access token"},
                status=status.HTTP_200_OK,
            )
        else:
            if self.verify_refresh_token(refresh_token):
                return redirect("custom_user:obtain-token")
            else:
                return Response(
                    {"message": "Invalid refresh token, please login"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(verification_token=kwargs["token"])
            user.is_verified = True
            user.verification_token = None
            user.verification_token_expiration = None
            user.save()
            tasks.account_verified_event.delay(
                initiator=user.email, user_id=user.id, payload={"email": user.email}
            )
            # Kafka event "account_verified" is sent here
            kafka_producers.kafka_user_account_verified_event(user.id)
            return Response({"message": "Email verified"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"message": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
