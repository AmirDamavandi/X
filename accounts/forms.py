from django import forms
import re

from sqlparse import parse

from .models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import phonenumbers


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=128)
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput, max_length=128,
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        username_pattern = r'^[a-zA-Z0-9._]{3,30}$'
        if not re.match(username_pattern, cleaned_data['username']):
            self.add_error('username', ValidationError('Username must contain only letters, numbers underscore and dot'))
        elif re.match(username_pattern, cleaned_data['username']):
            cleaned_data['username'] = cleaned_data['username'].lower()

        if cleaned_data['password1'] != cleaned_data['password2']:
            self.add_error('password2', ValidationError('Passwords must match'))

        password_pattern = r'[a-zA-Z0-9@$%&*_=+\']{6,128}'
        if not re.match(password_pattern, cleaned_data['password1']):
            self.add_error('password1', ValidationError(
                'Password must contain only letters(a-z, A-Z), numbers and some special characters, yours is invalid'
            ))
        elif re.match(password_pattern, cleaned_data['password1']):
            cleaned_data['password1'] = cleaned_data['password1']

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username', max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Email, Phone or Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        authenticating = authenticate(username=username, password=password)
        if not authenticating:
            query = User.objects.filter(username=username).exists()
            if not query:
                self.add_error('username', 'Incorrect username or password.')
            else:
                self.add_error('password', 'Incorrect password.')
        return self.cleaned_data


class UserEditModelForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            'is_verified', 'date_joined', 'relation', 'is_admin',
            'is_active', 'is_suspended', 'is_verified', 'password', 'last_login'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first-name', 'placeholder': ' '}),
            'last_name': forms.TextInput(attrs={'id': 'last-name', 'placeholder': ' '}),
            'username': forms.TextInput(attrs={'id': 'email', 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': ' '}),
            'phone_number': forms.TextInput(attrs={'id': 'phone', 'placeholder': ' '}),
            'bio': forms.Textarea(attrs={'id': 'bio', 'placeholder': ' ', 'rows': 2}),
            'gender': forms.Select(attrs={'id': 'gender', 'placeholder': ' '}),
            'date_of_birth': forms.DateInput(attrs={'id': 'dob', 'placeholder': ' '}),
            'account_type': forms.Select(attrs={'id': 'account_type', 'placeholder': ' '}),
            'location': forms.TextInput(attrs={'id': 'location', 'placeholder': ' '}),
            'website': forms.TextInput(attrs={'id': 'website', 'placeholder': ' '}),
            'header': forms.ClearableFileInput(attrs={'id': 'header-input', 'hidden': 'hidden'}),
            'avatar': forms.ClearableFileInput(attrs={'id': 'avatar-input', 'hidden': 'hidden'}),

        }


    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number is None:
            try:
                parsed_phone_number = phonenumbers.parse(phone_number)
                is_a_valid_phone_number = phonenumbers.is_valid_number(parsed_phone_number)
                if is_a_valid_phone_number:
                    self.cleaned_data['phone_number'] = parsed_phone_number
                else:
                    raise ValidationError('Enter a valid phone number')
            except phonenumbers.NumberParseException:
                raise ValidationError('Enter phone number with country code, like "+code" ')

        return phone_number
