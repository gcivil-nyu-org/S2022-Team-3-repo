from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .models import LoginAttempt, User
from .token import account_activation_token
from .decorators import unauthenticated_user
from .utils import send_user_email
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import PasswordResetForm, SetPasswordForm
from recycle.models import ZipCode
from django.utils.html import strip_tags


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    email_template_name = "email/email-forgot-password.html"
    success_url = reverse_lazy("accounts:password-reset-sent")
    subject_template_name = "email/password-reset-subject.txt"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy("accounts:password-reset-complete")


@unauthenticated_user
def signup_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")

        if not first_name:
            messages.error(request, "First name is required")
        elif not last_name:
            messages.error(request, "Last name is required")
        elif not email:
            messages.error(request, "Email is required")
        elif not password:
            messages.error(request, "Password is required")
        elif len(User.objects.filter(email=email)) > 0:
            messages.error(request, "User already exists")
            # Unable to find a user, this is fine
        else:
            try:
                user = User(
                    email=email,
                    first_name=first_name.title(),
                    last_name=last_name.title(),
                )
                user.set_password(password)
                user.is_active = False
                user.staff = False
                user.admin = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activate your account"
                response = send_user_email(
                    user,
                    mail_subject,
                    email,
                    current_site,
                    "email/email-verification.html",
                    "email/email-verification-no-style.html",
                )
                if response == "success":
                    messages.success(
                        request,
                        "We have sent you an activation link in your email. "
                        "Please confirm your "
                        "email to continue. Check your spam folder if you don't receive it",
                    )
                else:
                    messages.error(
                        request,
                        "An error occurred. Please ensure you have good internet connection "
                        "and you have entered a valid email address",
                    )
                    user.delete()
            except Exception:
                messages.error(
                    request,
                    "An error occurred. Please ensure you have good internet connection.",
                )
                if user:
                    user.delete()
    context = {}
    return render(request, "accounts/templates/signup.html", context)


def account_exists(request):

    """
    Users trying to login using Gauth but the email already exists as registered
    """
    messages.error(request, "Email already exists, please login using Login now button below")

    context = {}
    return render(request, "accounts/templates/login.html", context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        now = timezone.now()
        if not email:
            messages.error(request, "Email is required")
        elif not password:
            messages.error(request, "Password is required")
        else:
            try:
                _user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                messages.error(request, "Incorrect email or password")
                return redirect(settings.LOGIN_URL)

            login_attempt, _ = LoginAttempt.objects.get_or_create(
                user=_user
            )  # get the user's login attempt
            now = timezone.now()
            if (
                login_attempt.timestamp + timedelta(seconds=settings.LOGIN_ATTEMPTS_TIME_LIMIT)
            ) <= now:
                if not _user.is_active:
                    messages.error(request, "Please verify your email first.")
                    return redirect(settings.LOGIN_URL)
                else:
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        login(request, user)
                        login_attempt.login_attempts = 0  # reset the login attempts
                        login_attempt.save()
                        return redirect(settings.LOGIN_REDIRECT_URL)
                    else:
                        # if the password is incorrect, increment the login attempts and
                        # if the login attempts == MAX_LOGIN_ATTEMPTS,
                        # set the user to be inactive and send activation email
                        login_attempt.login_attempts += 1
                        login_attempt.timestamp = now
                        login_attempt.save()
                        if login_attempt.login_attempts == settings.MAX_LOGIN_ATTEMPTS:
                            _user.is_active = False
                            _user.save()
                            # send the re-activation email
                            mail_subject = "Account suspended"
                            current_site = get_current_site(request)
                            send_user_email(
                                _user,
                                mail_subject,
                                email,
                                current_site,
                                "email/email-account-suspended.html",
                                "email/email-account-suspended-no-style.html",
                            )
                            messages.error(
                                request,
                                "Account suspended, maximum login attempts exceeded. "
                                "Reactivation link has been sent to your email",
                            )
                        else:
                            messages.error(request, "Incorrect email or password")
                        return redirect(settings.LOGIN_URL)
            else:
                messages.error(request, "Login failed, please try again")
                return redirect(settings.LOGIN_URL)

    next = request.GET.get("next")
    if next:
        messages.error(request, "Login is required to access.")
    context = {}
    return render(request, "accounts/templates/login.html", context)


def activate_account_page(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login_attempt, _ = LoginAttempt.objects.get_or_create(user=user)
        if login_attempt.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            login_attempt.login_attempts = 0
            login_attempt.save()
            messages.success(request, "Account restored, you can now proceed to login")
        else:
            messages.success(
                request,
                "Thank you for confirming your email. You can now login.",
            )
        return redirect(settings.LOGIN_URL)
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect(settings.LOGIN_URL)


@login_required
def logout_view(request):

    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(settings.LOGOUT_REDIRECT_URL)


"""
function: user-profile

set path for user-profile
"""


@login_required
def user_profile(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get("first_name")
        if first_name:
            user.first_name = strip_tags(first_name)
        else:
            messages.error(request, "First name is required")
            return redirect("accounts:user-profile")

        last_name = request.POST.get("last_name")

        if last_name:
            user.last_name = strip_tags(last_name)
        else:
            messages.error(request, "Last name is required")
            return redirect("accounts:user-profile")

        phone_number = request.POST.get("phone_number")
        if phone_number:
            if len(phone_number) != 10 or not phone_number.isdigit():
                messages.error(
                    request,
                    "Please enter a valid 10 digit phone number. "
                    "Just include numbers without country code or any special symbols.",
                )
                return redirect("accounts:user-profile")
        else:
            phone_number = None
        user.phone_number = phone_number

        zipcode = request.POST.get("zipcode")
        zip_code = ZipCode.objects.filter(zip_code=zipcode)
        if zipcode == "" or zipcode is None:
            zipcode = None
        elif len(zip_code) == 0:
            messages.error(request, "Please enter a valid 5 digit NYC zipcode")
            return redirect("accounts:user-profile")
        else:
            zip_code = zip_code[0]
            user.zipcode = zip_code

        user.save()
        messages.success(request, "Your details have been updated successfully")
        return redirect("accounts:user-profile")
    return render(request, "accounts/templates/user-profile.html", {})


@login_required
def user_profile_avatar(request):
    if request.method == "POST":
        user = request.user
        avatar = request.POST.get("avatar")
        if avatar:
            user.avatar = avatar
        else:
            user.avatar = user.avatar
        user.save()
        messages.success(request, "Your avatar has been updated.")
    return redirect("accounts:user-profile")
