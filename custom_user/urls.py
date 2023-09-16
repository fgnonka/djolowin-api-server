from django.urls import path
from .views import (
    HomeView,
    LoginAPIView,
    LogoutAPIView,
    ObtainNewAccessTokenView,
    PasswordResetAPIView,
    PasswordResetRequestAPIView,
    RequestEmailVerificationView,
    SignupView,
    UserProfileView,
    ValidateTokenView,
    VerifyEmailView,
    UserWalletDashboardAPIView
)
from .google.google import GoogleAuthAPIView

app_name = "custom_user"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("obtain-token/", ObtainNewAccessTokenView.as_view(), name="obtain-token"),
    path("password-reset/<str:token>/", PasswordResetAPIView.as_view(), name="password-reset"),
    path(
        "password-reset-request/",
        PasswordResetRequestAPIView.as_view(),
        name="password-reset-request",
    ),
    path(
        "request-email-verification/",
        RequestEmailVerificationView.as_view(),
        name="request-email-verification",
    ),
    path("signup/", SignupView.as_view(), name="signup"),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path("validate-token/", ValidateTokenView.as_view(), name="validate-token"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("api/google-oauth/", GoogleAuthAPIView.as_view(), name="google-oauth"),
    path("wallet/dashboard/", view=UserWalletDashboardAPIView.as_view(), name="wallet-dashboard"),
]
