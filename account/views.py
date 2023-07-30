from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import generic, View
from django.views.generic import DetailView, RedirectView, UpdateView

from core.mixins import CustomDispatchMixin, PageTitleMixin

from .broadcast import send_email_change_request
from .events import *
from .forms import UserRegistrationForm, UserUpdateForm
from .tokens import account_activation_token, decode_token_check, encode_token
from .decorators import user_is_active
from .signals import user_verified

User = get_user_model()


USER_MODEL_MISMATCH = """
The registration view ({view}) is using the form class {form},
but the model used by the form ({form_model}) is not your Django installation's user model ({user_model}).
Please use a custom registration form class compatible with your custom user model.
See django-registration's documentation on custom user models for more details.
"""


class ActivateAccountView(View):
    """Activate a user's account by verifying their email address."""

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if decode_token_check(uidb64, token):
            user.is_active = True
            user.save()
            # Log the user in, redirect to their dashboard, or show a success message
            messages.success(
                request,
                _("Your account has been successfully verified. You can now login."),
            )
            customer_user_account_verified_event(user=user)
            return redirect("account:login")
        else:
            # Display an 'Invalid activation link' error message
            return render(request, "djolowin/account/activation_invalid.html")


class SignupView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = "djolowin/account/signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            customer_user_signup_event(user=user)
            customer_verification_email_sent_event(user=user)
            return render(
                request,
                "djolowin/account/verification_email_sent.html",
                {"email": user.email},
            )
        return render(request, self.template_name, {"form": form})


user_signup_view = SignupView.as_view()


class CustomLoginView(LoginView):
    template_name = "djolowin/account/new_login.html"

    def get_failed_login_attempts_key(self, username):
        return f"failed_login_attempts_{username}"

    def get_success_url(self):
        user = self.request.user
        customer_user_login_successful_event(user=user)
        return reverse_lazy(
            settings.LOGIN_REDIRECT_URL,
        )

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        # Reset the failed attempts count if the login is successful
        failed_attempts_key = self.get_failed_login_attempts_key(username)
        cache.delete(failed_attempts_key)
        return super().form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get("username")
        # Get the current number of failed login attempts for the user
        failed_attempts_key = self.get_failed_login_attempts_key(username)
        failed_attempts_count = cache.get(failed_attempts_key, 0)
        failed_attempts_count += 1
        cache.set(
            failed_attempts_key,
            failed_attempts_count,
            timeout=settings.LOGIN_ATTEMPTS_TIMEOUT,
        )
        # print(cache.get(failed_attempts_key))
        # If the number of failed attempts exceeds the limit, block the login temporarily
        if failed_attempts_count >= settings.MAX_LOGIN_ATTEMPTS:
            return render(
                self.request,
                "djolowin/account/login_locked.html",
                {"username": username},
            )
        customer_user_login_failed_event(parameters=username)
        return super().form_invalid(form)


user_login_view = CustomLoginView.as_view()


class RequestActivationEmailView(View):
    template_name = "djolowin/account/request_activation_email.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_email = request.POST.get("email")
        user = User.objects.filter(email=user_email).first()
        customer_new_verification_email_requested_event(user=user)

        if user and not user.is_active:
            # Generate the token
            uid, token = encode_token(user)

            # Send the activation email
            subject = "Activate your account"
            message = render_to_string(
                "djolowin/account/activation_email.html",
                {
                    "user": user,
                    "protocol": "http",
                    "domain": request.get_host(),
                    "uid": uid,
                    "token": token,
                },
            )
            email = EmailMessage(subject, message, to=[user.email])
            email.send()
            customer_new_verification_email_sent_event(user=user)
            messages.success(
                request, _("Activation email sent. Please check your inbox.")
            )
            return render(
                request,
                "djolowin/account/verification_email_sent.html",
                {"email": user_email},
            )

        messages.error(
            request, _("Email not found or the account is already activated.")
        )
        return render(request, self.template_name)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "djolowin/account/user/user_detail.html"
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "country",
        "profile_img",
        "date_joined",
    ]

    def get_object(self, queryset=None):
        return self.request.user


user_detail_view = UserDetailView.as_view()


class UserUpdateView(
    PageTitleMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    template_name = "djolowin/account/user/user_form.html"
    model = User
    form_class = UserUpdateForm
    page_title = _("Update account")
    active_tab = "account"
    success_message = _("Your account information has been successfully updated")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        session_user = self.request.user
        assert session_user.is_authenticated
        return session_user.get_absolute_url()

    def form_valid(self, form):
        try:
            old_user = User.objects.get(pk=self.request.user.pk)
        except User.DoesNotExist:
            old_user = None
        # We need to check if the email of the user has changed.
        new_email = form.cleaned_data.get("email")
        if new_email and old_user and old_user.email != new_email:
            # If it has, we need to send a confirmation email to the old address
            # in case the user has been hacked.
            send_email_change_request(old_user, new_email)
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse_lazy(
            settings.DJOLOWIN_ACCOUNTS_REDIRECT_URL,
            kwargs={"username": self.request.user.username},
        )


def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    print(data)
    return JsonResponse(data)


user_redirect_view = UserRedirectView.as_view()
