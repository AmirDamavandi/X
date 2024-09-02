from django import forms
import re as regex


class SignupForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    username = forms.CharField(label='Username', max_length=60)
    email = forms.EmailField(label='Email Address')
    phone_number = forms.CharField(label='Phone Number', max_length=13)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        username_pattern = r'[a-zA-Z0-9]+(._)?'
        # if User.objects.filter(username=username).exists():
        #     raise forms.ValidationError('Username already exists')
        if not regex.match(username_pattern, username):
            raise forms.ValidationError('Invalid username')
        return username

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
