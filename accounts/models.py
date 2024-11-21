from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import MyUserManager
from django.core.exceptions import ValidationError
import re
from urllib.parse import urlparse
from tweets.models import View as PostView, Tweet, Like, Retweet, Bookmark
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
    relation = models.ManyToManyField('Relation', related_name='user_following')
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
        followers = self.follower.count()
        return followers

    def following_count(self):
        followings = self.following.count()
        return followings

    def following_check(self, user):
        relation_check = Relation.objects.filter(from_user=user, to_user=self).exists()
        return relation_check

    def retweet_count(self):
        retweets = Retweet.objects.filter(user=self).count()
        return retweets

    def like_count(self):
        likes = Like.objects.filter(user=self).count()
        return likes

    def bookmark_count(self):
        bookmarks = Bookmark.objects.filter(user=self).count()
        return bookmarks

    def comment_count(self):
        comments = Tweet.objects.filter(user=self, comment__isnull=False).count()
        return comments

    def user_tweets(self):
        all_tweets = []
        tweets = Tweet.objects.filter(user=self)
        retweets = Retweet.objects.filter(user=self)
        all_tweets += tweets
        for tweet in retweets:
            all_tweets.append(tweet.tweet)
        all_tweets = sorted(all_tweets, key=lambda x: x.created_at, reverse=True)
        return all_tweets

    def tweets_count(self):
        tweets = Tweet.objects.filter(user=self).count()
        retweets = Tweet.objects.filter(user=self).count()
        result = tweets + retweets
        return result


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.to_user}'

    class Meta:
        unique_together = (('from_user', 'to_user'),)
        verbose_name = _('relation')

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError('users cannot follow themselves')
        if Relation.objects.filter(from_user=self.from_user, to_user=self.to_user).exists():
            raise ValidationError('user follows user already')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, *kwargs)


class ConnectPeople(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='self')
    linked_user = models.ForeignKey(User, related_name='people', on_delete=models.CASCADE)
    link_reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.linked_user} linked to {self.user}'

    class Meta:
        unique_together = (('user', 'linked_user'),)
        verbose_name = _('connect people')
        verbose_name_plural = _('connect people')
        
    def clean(self):
        if self.user == self.linked_user:
            raise ValidationError('users cannot link to themselves')
        elif ConnectPeople.objects.filter(user=self.user).count() >= 5:
            raise ValidationError('user cannot have more than 5 linked user')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, *kwargs)

