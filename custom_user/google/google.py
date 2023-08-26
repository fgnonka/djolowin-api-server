from django.conf import settings
from django.urls import reverse

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .. import tasks
from ..models import CustomUser as User, UserWallet
from ..send_email import send_verification_email

FRONTEND_URL = settings.DJOLOWIN_FRONTEND_URL

class GoogleAuthAPIView(APIView):
    def post(self, request):
        # Get the token from the request
        token = request.data.get("token")
        # Verify the token
        googleUser = id_token.verify_oauth2_token(token, GoogleRequest(), clock_skew_in_seconds=10)
        # If the token is invalid, return an error
        if not googleUser:
            tasks.signup_attempt_failed_event(
            initiator=request.META.get("REMOTE_ADDR"),
            payload={"ip_address": request.META.get("REMOTE_ADDR"), 'provider': 'google', 'email': request.data.get("token")},
        )
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(email=googleUser["email"]).first()

        # If there is no user with this email, create one
        if not user:
            user = User.objects.create(
                email=googleUser["email"],
                username=googleUser["email"],
                first_name=googleUser["given_name"],
                last_name=googleUser["family_name"],
                is_active=True,
                auth_provider="google",
            )
            user.set_password(User.objects.make_random_password())
            user.save()
            # Create a wallet for the user
            UserWallet.objects.create(user_id=user.id)
            relative_link = reverse(
            "custom_user:verify-email", kwargs={"token": str(user.verification_token)}
        )
            verify_link = f"{FRONTEND_URL}{relative_link}"
            send_verification_email(user, verify_link)
            ip_address = request.META.get("REMOTE_ADDR")    
            tasks.signup_attempt_successful_event(
                user_id=user.id,
                initiator=user.email,
                payload={"ip_address": ip_address, "email": googleUser["email"], 'provider': 'google'},
            )
            return Response(
                {"message": "Account created successfully. Please check your email for verification."},
                status=status.HTTP_201_CREATED,
            )
        # If the user exists, check if they are verified
        if not user.is_verified:
            return Response({"message": "Your account is not yet verified. Please check your email for verification."}, status=status.HTTP_400_BAD_REQUEST)
        
        # If the user exists, generate new refresh and access tokens
        refresh_token = user.tokens()["refresh"]
        access_token = user.tokens()["access"]
        response = Response()
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        response.data = {
            "email": user.email,
            "tokens": {
                "refresh": refresh_token,
                "access": access_token,
            },
        }
        tasks.successful_login_event(
            user_id=user.id,
            initiator=user.email,
            payload={"ip_address": request.META.get("REMOTE_ADDR"), 'provider': 'google', 'email': user.email},
        )
        return response
