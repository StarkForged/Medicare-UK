from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class LoginForm(AuthenticationForm):
    """
    Inherits all validation from Django's built-in AuthenticationForm.
    We just customise the placeholder text on the inputs.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class RegisterForm(UserCreationForm):
    """
    Extends Django's UserCreationForm (which already handles
    password hashing, password confirmation, etc.) with our extra fields.
    """
    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'role', 'organisation', 'phone',
            'password1', 'password2',
        ]
