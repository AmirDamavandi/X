from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import MyUserManager
from django.core.exceptions import ValidationError


# Create your models here.

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30, help_text='enter your first name')
    last_name = models.CharField(max_length=30, help_text='enter your last name', blank=True, null=True)
    header = models.ImageField(upload_to='users_header/', null=True, blank=True)
    avatar = models.ImageField(upload_to='users_avatar/', null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, help_text='enter your username')
    email = models.EmailField(unique=True, help_text='enter your email address', blank=True, null=True)
    phone_number = models.CharField(
        max_length=11, unique=True, help_text='enter your phone number', blank=True, null=True
    )
    is_verified = models.BooleanField(default=False)
    account_types = (('public', 'Public'), ('private', 'Private'))
    account_type = models.CharField(max_length=8, choices=account_types, default='public')
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    genders = (('male', 'Male'), ('female', 'Female'), ('prefer not to say', 'Prefer not to say'))
    gender = models.CharField(max_length=17, choices=genders)
    is_suspended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def clean(self):
        if not self.email and not self.phone_number:
            raise ValidationError("Either email or phone number must be provided.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

