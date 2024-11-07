from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tweets')
    tweet = models.TextField(max_length=1000, db_index=True)
    status = models.BooleanField(default=True)
    comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True)
    quote_tweet = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='quote_tweets',
        blank=True,
        null=True
    )
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PostView', related_name='views')
    retweet = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Retweet', related_name='retweets')
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like', related_name='likes')
    bookmark = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Bookmark', related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tweet

    def clean(self):
        if self.comment and self.quote_tweet:
            raise ValidationError('you cannot comment and quote a tweet at the same time')
        if Tweet.objects.filter(quote_tweet=self.quote_tweet, user=self.user).exists():
            raise ValidationError('you cannot retweet a tweet twice')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Tweet',)
        verbose_name_plural = _('Tweets',)



class PostView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_views')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweet_views')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed {self.tweet}'

    class Meta:
        verbose_name = _('Post View',)
        verbose_name_plural = _('Post Views',)


class Retweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_retweets')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweet_retweets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} retweeted {self.tweet}'

    def clean(self):
        exists = Retweet.objects.filter(user=self.user, tweet=self.tweet).exists()
        if exists:
            raise ValidationError('user already retweeted this tweet')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Retweet',)
        verbose_name_plural = _('Retweets',)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweet_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} liked {self.tweet}'

    def clean(self):
        exists = Like.objects.filter(user=self.user, tweet=self.tweet).exists()
        if exists:
            raise ValidationError('user already liked this tweet')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Like',)
        verbose_name_plural = _('Likes',)

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_bookmarks')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweet_bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} bookmarked {self.tweet}'

    def clean(self):
        exists = Bookmark.objects.filter(user=self.user, tweet=self.tweet).exists()
        if exists:
            raise ValidationError('user already bookmarked this tweet')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Bookmark',)
        verbose_name_plural = _('Bookmarks',)