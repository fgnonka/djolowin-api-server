import unicodedata
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import exceptions, validators
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.app_settings import AuthenticationMethod
from allauth.account.forms import BaseSignupForm
from allauth.account.utils import (
    get_user_model,
    perform_login,
    setup_user_email,
    user_email,
    user_username,
)


from allauth.utils import (
    set_form_field_order,
    build_absolute_uri,
)

UserModel = get_user_model()


class CustomEmailField(forms.EmailField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "email",
        }


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop(
            "render_value", app_settings.PASSWORD_INPUT_RENDER_VALUE
        )
        kwargs["widget"] = forms.PasswordInput(
            render_value=render_value,
            attrs={"placeholder": kwargs.get("label")},
        )
        autocomplete = kwargs.pop("autocomplete", None)
        if autocomplete is not None:
            kwargs["widget"].attrs["autocomplete"] = autocomplete
        super(PasswordField, self).__init__(*args, **kwargs)


class CustomLoginForm(forms.Form):
    email = CustomEmailField(label=_("E-mail"), max_length=254)
    password = PasswordField(label=_("Password"), autocomplete="current-password")
    remember = forms.BooleanField(label=_("Remember Me"), required=False)

    user = None
    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "email_password_mismatch": _(
            "The e-mail address and/or password you specified are not correct."
        ),
        "username_password_mismatch": _(
            "The username and/or password you specified are not correct."
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        set_form_field_order(self, ["email", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]

    def user_credentials(self):
        """
        Provides the credentials required to authenticate the user for
        login.
        """
        credentials = {}
        email = self.cleaned_data["email"]
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            credentials["email"] = email
        else:
            if self._is_login_email(email):
                credentials["email"] = email
        credentials["password"] = self.cleaned_data["password"]
        return credentials

    def _is_login_email(self, login):
        try:
            validators.validate_email(login)
            ret = True
        except exceptions.ValidationError:
            ret = False
        return ret

    def clean(self):
        super(CustomLoginForm, self).clean()
        if self._errors:
            return
        credentials = self.user_credentials()
        user = get_adapter(self.request).authenticate(self.request, **credentials)
        if user:
            self.user = user
        else:
            raise forms.ValidationError(
                self.error_messages["email_password_mismatch"],
            )
        return self.cleaned_data

    def login(self, request, redirect_url=None):
        email = self.user_credentials().get("email")
        ret = perform_login(
            request,
            self.user,
            email_verification=app_settings.EMAIL_VERIFICATION,
            redirect_url=redirect_url,
            email=email,
        )
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data["remember"]
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret

    def is_valid(self) -> bool:
        return super().is_valid()

    def get_user(self):
        return self.user


class CustomSignupForm(BaseSignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields["password1"] = PasswordField(
            label=_("Password"), autocomplete="new-password"
        )
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields["password2"] = PasswordField(
                label=_("Password (again)"), autocomplete="new-password"
            )

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

    def clean(self):
        super(CustomSignupForm, self).clean()

        # `password` cannot be of type `SetPasswordField`, as we don't
        # have a `User` yet. So, let's populate a dummy user to be used
        # for password validation.
        User = get_user_model()
        dummy_user = User()
        user_username(dummy_user, self.cleaned_data.get("username"))
        user_email(dummy_user, self.cleaned_data.get("email"))
        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=dummy_user)
            except forms.ValidationError as e:
                self.add_error("password1", e)

        if (
            app_settings.SIGNUP_PASSWORD_ENTER_TWICE
            and "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    _("You must type the same password each time."),
                )
        return self.cleaned_data

    def save(self, request):
        if self.account_already_exists:
            # Don't create a new acount, only send an email informing the user
            # that (s)he already has one...
            self._send_account_already_exists_mail(request)
            return
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user

    def _send_account_already_exists_mail(self, request):
        signup_url = build_absolute_uri(request, reverse("account_signup"))
        password_reset_url = build_absolute_uri(
            request, reverse("account_reset_password")
        )
        email = self.cleaned_data["email"]
        context = {
            "request": request,
            "current_site": get_current_site(request),
            "email": email,
            "signup_url": signup_url,
            "password_reset_url": password_reset_url,
        }
        get_adapter(request).send_mail(
            "account/email/account_already_exists", email, context
        )

    def is_valid(self) -> bool:
        return super().is_valid()
