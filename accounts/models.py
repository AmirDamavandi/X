import re

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import MyUserManager
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
# Create your models here.


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30, help_text='enter your first name')
    last_name = models.CharField(max_length=30, help_text='enter your last name', blank=True, null=True)
    header = models.ImageField(upload_to='users_header/', null=True, blank=True)
    avatar = models.ImageField(upload_to='users_avatar/', null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, help_text='enter your username')
    email = models.EmailField(unique=True, help_text='enter your email address')
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

    def clean(self):
        username_pattern = r'^[a-zA-Z0-9._]{3,30}$'
        if not re.match(username_pattern, self.username):
            raise ValidationError('Username must contain only letters, numbers underscore and dot')
        else:
            self.username = self.username.lower()

        password_pattern = r'^[a-zA-Z0-9@$%&*_=+\']{6,128}$'
        if not re.match(password_pattern, self.password):
            raise ValidationError(
                'Password must contain only letters(a-z, A-Z), numbers and some special characters, yours is invalid'
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name

    def header_image(self):
        if self.header:
            return self.header.url

    def avatar_image(self):
        if self.avatar:
            return self.avatar.url

    def user_website(self):
        if self.website:
            domain = urlparse(self.website)
            return domain.netloc

    def birthdate_format(self):
        birthdate = self.date_of_birth.strftime('%B %d').replace('0', '')
        return birthdate

    def date_joined_format(self):
        date_joined = self.date_joined.strftime('%B %Y')
        return date_joined

    def follower_count(self):
        return self.follower.count()

    def following_count(self):
        return self.following.count()

    def following_check(self, user):
        return Relation.objects.filter(from_user=user, to_user=self).exists()


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} followed {self.to_user}'

    class Meta:
        unique_together = (('from_user', 'to_user'),)
        verbose_name = _('relation')
        verbose_name_plural = _('relations')

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError('users cannot follow themselves')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, *kwargs)
