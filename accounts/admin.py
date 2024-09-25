from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *

# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'date_of_birth', 'is_active', 'is_admin']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        'first_name', 'last_name', 'username', 'email', 'date_joined',
        'phone_number', 'is_verified', 'gender', 'is_suspended', 'is_admin'
    ]
    list_filter = ['is_admin', 'is_verified', 'is_suspended', 'date_joined', 'date_of_birth']
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Personal info', {'fields': [
            'first_name', 'last_name',
            'gender', 'date_of_birth'
        ]}),
        ('Account info', {'fields': [
            'header', 'avatar', 'username', 'phone_number', 'account_type', 'bio',
            'location', 'website', 'is_suspended'
        ]}),
        ('Verify', {'fields': ['is_verified', 'is_active']}),
        ('Permissions', {'fields': ['is_admin']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['first_name', 'username', 'email', 'password1', 'password2'],
            },
        ),
    ]
    search_fields = ['email', 'username', 'first_name']
    ordering = ['email']
    filter_horizontal = []


admin.site.register(User, UserAdmin)


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'followed_at']
