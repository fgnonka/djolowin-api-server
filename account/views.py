from datetime import datetime, timedelta

from .new_tasks import login_attempt_event

from django.conf import settings
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    get_user_model,
    authenticate,
)
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework_simplejwt.tokens import RefreshToken, BlacklistMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from core.mixins import ClientIPMixin

from . import CustomerEvents

from . import tasks
from .forms import CustomLoginForm, CustomSignupForm
from .mixins import VerifyLoggedInMixin, TokenDeleteMixin
from .models import CustomUser as User
from .send_email import send_verification_email, send_reset_password_email
from .serializers import UserSerializer
from .mixins import (
    TokenExpirationMixin,
    TokenVerificationMixin,
    # JWTAuthenticationFromCookieMixin,
)
from .validation_functions import (
    validate_credentials_at_registration,
)

User = get_user_model()


class SignupView(APIView, ClientIPMixin, TokenExpirationMixin):
    authentication_classes = []

    def post(self, request):
        print(request.data)
        ip_address = self.get_client_ip(request)
        form = CustomSignupForm(data=request.data)
        form_email = request.data.get("email")
        tasks.signup_attempt_event(
            payload={"ip_address": ip_address, "email": form_email}
        )
        validate_credentials_at_registration(request)
        if form.is_valid():
            try:
                user = form.save(request)
                created_user = User.objects.filter_by_email(email=user.email).first()
                created_user.save()
                tasks.account_created_event(
                    user_id=created_user.id,
                    payload={
                        "email": created_user.email,
                        "status": str(status.HTTP_201_CREATED),
                    },
                )
                send_verification_email(created_user)
                return Response(
                    {
                        "message": "User registered successfully.",
                        "user": user.email,
                        "id": user.id,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as error:
                return Response(
                    {"error": str(error)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"message": "User registration failed.", "errors": form.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


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


class LoginAPIView(APIView, ClientIPMixin, VerifyLoggedInMixin):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request):
        print(request.session.items())
        logged_in_user = self.verify_logged_in_user(request)
        if logged_in_user:
            return Response(
                {
                    "message": "User already logged in",
                    "user": logged_in_user.email,
                    "user_id": logged_in_user.id,
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        ip_address = self.get_client_ip(request)
        email = request.data.get("email")
        form = CustomLoginForm(request, data=request.data)
        login_attempt_event.delay(payload={"ip_address": ip_address, "email": email})

        if form.is_valid():
            user = authenticate(
                request, email=email, password=form.cleaned_data["password"]
            )
            user_id = user.id
            auth_login(request, user)
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            tasks.access_token_generated_event(user_id=user_id)
            tasks.refresh_token_generated_event(user_id=user_id)
            response = Response(
                {
                    "message": "Login successful.",
                    "user": user.email,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
            response.set_cookie("refresh_token", str(refresh_token), httponly=True)
            response.set_cookie(settings.AUTH_COOKIE, str(access_token), httponly=True)

            tasks.successful_login_event(
                user_id=user_id,
                payload={"ip_address": ip_address, "status": str(status.HTTP_200_OK)},
            )

            return response
        else:
            tasks.failed_login_attempt_event(
                payload={
                    "ip_address": ip_address,
                    "email": email,
                    "status": str(status.HTTP_400_BAD_REQUEST),
                }
            )
            return Response(
                {"message": "Invalid email or password.", "errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )


class LogoutView(APIView, TokenDeleteMixin):
    def post(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Logout the user, which invalidates the session and refresh token
            auth_logout(request)
            # Clear the session data, including the refresh token and access token
            self.delete_tokens(request)

            response = Response(
                {"message": "Logout successful."}, status=status.HTTP_200_OK
            )
            # Return a success response
            return response
        else:
            # If the user is not authenticated, return an error response
            return Response(
                {"error": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


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
                    tasks.access_token_generated_event(
                        user_id=payload_user_id, payload={"expiration": json_expiration}
                    )
                    response = Response(
                        {
                            "message": f"Access token refreshed {access_token} ",
                            "access_token": str(access_token),
                        },
                        status=status.HTTP_200_OK,
                    )
                    return response
                else:
                    print("Invalid or expired refresh token")
                    return Response(
                        {"message": "Invalid or expired refresh token"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except TokenError as e:
                print("Invalid or expired refresh token 2")
                return Response(
                    {"message": "Invalid or expired refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            print("No refresh token in session")
            return Response(
                {"message": "No refresh token in session. Please login again."},
                status=status.HTTP_401_UNAUTHORIZED,
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

        # Send the reset password link to the user's email
        send_reset_password_email(user)

        return Response(
            {"message": "Password reset link sent to your email."},
            status=status.HTTP_200_OK,
        )


class PasswordResetAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        reset_token = kwargs["token"]
        password = request.data.get("password")
        if not password:
            return Response(
                {"message": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(reset_password_token=reset_token)
        except User.DoesNotExist:
            return Response(
                {"message": "Invalid or expired reset token."},
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
        user.set_password(password)
        user.reset_password_token = None
        user.reset_password_token_expiration = None
        user.save()

        return Response(
            {"message": "Password reset successfully."}, status=status.HTTP_200_OK
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
                send_verification_email(user)
                return Response(
                    {"message": "Verification email sent"},
                    status=status.HTTP_200_OK,
                )
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserDetailView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            user = request.user
            if not user.is_authenticated:
                return Response(
                    {"message": "You are not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist or AttributeError:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


# --------------------------------------------------------------------------------
class VerifyEmailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(verification_token=kwargs["token"])
            user.is_verified = True
            user.verification_token = None
            user.verification_token_expiration = None
            user.save()
            return Response({"message": "Email verified"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
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
                return redirect("account:obtain-token")
            else:
                return Response(
                    {"message": "Invalid refresh token, please login"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
