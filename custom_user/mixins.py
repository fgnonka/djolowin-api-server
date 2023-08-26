from datetime import datetime, timedelta

from django.conf import settings

from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# from .cookie_auth import JWTAuthenticationFromCookie
from .models import CustomUser


# class JWTAuthenticationFromCookieMixin(JWTAuthenticationFromCookie):
#     authentication_classes = [JWTAuthenticationFromCookie]


class TokenExpirationMixin:
    def get_token_expiration(self) -> datetime:
        return datetime.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]


class TokenVerificationMixin:
    def verify_access_token(self, access_token: str) -> bool:
        try:
            decoded = AccessToken(access_token)
            expiration_time = decoded.payload["exp"]
            expiration_datetime = datetime.fromtimestamp(expiration_time)

            return expiration_datetime > datetime.now()
        except TokenError as e:
            return False

    def verify_refresh_token(self, refresh_token: str) -> bool:
        try:
            decoded = RefreshToken(refresh_token)
            expiration_time = decoded.payload["exp"]
            expiration_datetime = datetime.fromtimestamp(expiration_time)
            if expiration_datetime > datetime.now():
                return True
            else:
                return False
        except TokenError as e:
            return False


class VerifyLoggedInMixin(TokenExpirationMixin, TokenVerificationMixin):
    def verify_logged_in_user(self, request):
        access_token = request.COOKIES.get(settings.AUTH_COOKIE)
        if not access_token:
            return None
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            encrypted_refresh_token = refresh_token
            # Check if both access token and refresh token are valid
            if self.verify_access_token(access_token) and self.verify_refresh_token(
                encrypted_refresh_token
            ):
                try:
                    access_token_payload = AccessToken(access_token).payload
                    user_id = access_token_payload["user_id"]
                    user = CustomUser.objects.get(id=user_id)
                    if user:
                        # User is already logged in and tokens are valid
                        return user
                except TokenError as e:
                    return None
        return None


class TokenDeleteMixin:
    def delete_tokens(self, request):
        response = Response()
        response.delete_cookie(settings.AUTH_COOKIE)
        response.delete_cookie("refresh_token")
        request.session.flush()
        return response
