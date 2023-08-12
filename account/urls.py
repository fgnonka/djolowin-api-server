from django.urls import path, reverse_lazy
from .views import (
    HomeView,
    LoginAPIView,
    LogoutView,
    ObtainNewAccessTokenView,
    PasswordResetAPIView,
    PasswordResetRequestAPIView,
    RequestEmailVerificationView,
    SignupView,
    UserDetailView,
    ValidateTokenView,
    VerifyEmailView,
)

app_name = "account"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
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
    path("user-detail/", UserDetailView.as_view(), name="user-detail"),
    path("validate-token/", ValidateTokenView.as_view(), name="validate-token"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
]
