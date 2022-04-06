from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import (
    PasswordResetForm as AuthPasswordResetForm,
    SetPasswordForm as AuthSetPasswordForm,
)
from django.forms.widgets import EmailInput
from django.utils.encoding import force_str as _

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all required fields plus
    repeated password"""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_password2(self):  # checking that the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):  # save he proovided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users, includes all the fields on the user, but
    replaces the password fields with admin's password hash display field."""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "admin")

    def clean_password(self):
        """Regardless of what the user provides retrun the initial value.
        This is done here rather than on the field, because the field does
        not have access to the initial value."""
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "Enter email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Enter password"}),
    )


class RegistrationForm(forms.ModelForm):
    """A form for creating new users. Includes all required fields plus
    repeated password"""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Enter password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "placeholder": "Confirm password"}
        ),
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "Enter Email"}),
            "first_name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter Last Name"}
            ),
        }

    def clean_password2(self):  # checking that the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):  # save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
        return user


class PasswordResetForm(AuthPasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        widget=EmailInput(
            attrs={
                "class": "validate form-control",
                "placeholder": "name@example.com",
                "required": "required",
                "name": "email",
            }
        ),
        label="Email",
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email, is_active=True).exists():
            msg = _("There is no user registered with the specified E-Mail address.")
            self.add_error("email", msg)
        return email


class SetPasswordForm(AuthSetPasswordForm):
    def __init__(self, *args, **kwargs):
        self.auto_id = False
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "validate form-control",
                "placeholder": "••••••••",
                "required": "required",
                "name": "password",
                "id": "password",
            }
        ),
        label="Password",
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "validate form-control",
                "placeholder": "••••••••",
                "required": "required",
                "name": "confirm_password",
                "id": "confirm-password",
            }
        ),
        label="Confirm Password",
    )

    def clean_password2(self):  # checking that the two passwords match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            msg = _("Password and confirm password do not match.")
            self.add_error("confirm_password", msg)
        return password1
