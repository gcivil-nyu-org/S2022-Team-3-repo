from audioop import reverse
from datetime import timedelta
from email import message
from click import password_option

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

# from .forms import RegistrationForm, LoginForm
from .models import LoginAttempt, User
from .token import account_activation_token
from .decorators import unauthenticated_user
from .utils import send_user_email


@unauthenticated_user
def signup_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not first_name:
            messages.error(request, 'First name is required')
        elif not last_name:
            messages.error(request, 'Last name is required')
        elif not email:
            messages.error(request, 'Email is required')
        elif not password:
            messages.error(request, 'Password is required')
        else:
            try:
                user = User(email=email, password=password, first_name=first_name, last_name=last_name)
                user.is_active = False
                user.is_staff = False
                user.is_admin = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                response = send_user_email(user, mail_subject, email, current_site, 'email/email_verification.html')
                if response == 'success':
                    messages.success(request, "We have sent you an activation link in your email. Please confirm your"
                                                "email to continue. Check your spam folder if you don't receive it")
                else:
                    messages.error(request, 'An error occurred. Please ensure you have good internet connection and you have entered a valid email address')
                    user.delete()
            except:
                messages.error(request, 'An error occurred. Please ensure you have good internet connection.')
                if user:
                    user.delete()
    context = {}
    return render(request, 'account/templates/signup.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':       
        email = request.POST.get('email')
        password = request.POST.get('password')
        now = timezone.now()
        if not email:
            messages.error(request, 'Email is required')
        elif not password:
            messages.error(request, 'Password is required')
        else:
            try:
                _user = User.objects.get(email=email)
                login_attempt, created = LoginAttempt.objects.get_or_create(user=_user)  # get the user's login attempt
                if (login_attempt.timestamp + timedelta(seconds=settings.LOGIN_ATTEMPTS_TIME_LIMIT)) < now:
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        if not _user.is_active:
                            messages.error(request, "Please verify your email first.")
                            return redirect(settings.LOGIN_URL)
                        else:
                            login(request, user)
                            login_attempt.login_attempts = 0    # reset the login attempts
                            login_attempt.save()
                            return redirect(settings.LOGIN_REDIRECT_URL)  # change expected_url in your project
                    else:
                        # if the password is incorrect, increment the login attempts and
                        # if the login attempts == MAX_LOGIN_ATTEMPTS, set the user to be inactive and send activation email
                        login_attempt.login_attempts += 1
                        login_attempt.timestamp = now
                        login_attempt.save()
                        if login_attempt.login_attempts == settings.MAX_LOGIN_ATTEMPTS:
                            _user.is_active = False
                            _user.save()
                            # send the re-activation email
                            mail_subject = "Account suspended"
                            current_site = get_current_site(request)
                            send_user_email(_user, mail_subject, email, current_site, 'email/email_account_suspended.html')
                            messages.error(request, 'Account suspended, maximum login attempts exceeded. '
                                                    'Reactivation link has been sent to your email')
                        else:
                            messages.error(request, 'Incorrect email or password')
                        return redirect(settings.LOGIN_URL)
                else:
                    messages.error(request, 'Login failed, please try again')
                    return redirect(settings.LOGIN_URL)

            except ObjectDoesNotExist:
                messages.error(request, 'Incorrect email or password')
                return redirect(settings.LOGIN_URL)

    context = {}
    return render(request, 'account/templates/login.html', context)


def activate_account_page(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login_attempt, created = LoginAttempt.objects.get_or_create(user=user)
        if login_attempt.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            login_attempt.login_attempts = 0
            login_attempt.save()
            messages.success(request, 'Account restored, you can now proceed to login')
        else:
            messages.success(request, 'Thank you for confirming your email. You can now login.')
        return redirect(settings.LOGIN_URL)
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect(settings.LOGIN_URL)

def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
