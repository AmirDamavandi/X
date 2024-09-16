from django import forms
import re as regex
from .models import User
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=128)
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput, max_length=128,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')
        if email is None and phone_number is None:
            self.add_error('email', 'Either email or phone number must be provided.')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        username_pattern = r'^[a-zA-Z0-9._]{3,30}$'
        if not regex.match(username_pattern, username):
            return self.add_error('username', 'Incorrect username.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        password_pattern = r'^[a-zA-Z0-9@$%&*_=+\']{6,128}$'
        if not regex.match(password_pattern, str(password1)):
            return self.add_error('password1', ValidationError('Incorrect password'))
        return password1


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username', max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Email, Phone or Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
