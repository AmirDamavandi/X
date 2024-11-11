from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
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
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, through='View', related_name='views')
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
        if Tweet.objects.filter(quote_tweet__isnull=False, quote_tweet=self.quote_tweet, user=self.user).exists():
            raise ValidationError('you cannot retweet a tweet twice')

    def save(self, *args, **kwargs):
        self.clean()
        super(Tweet, self).save(*args, **kwargs)

    def view_count(self):
        return View.objects.filter(tweet=self).count()

    def like_count(self):
        return Like.objects.filter(tweet=self).count()

    def retweet_count(self):
        return Retweet.objects.filter(tweet=self).count()

    def bookmark_count(self):
        return Bookmark.objects.filter(tweet=self).count()

    def user_tweeted(self):
        return self.user

    class Meta:
        verbose_name = _('Tweet',)
        verbose_name_plural = _('Tweets',)


class Hashtag(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='hashtags')
    hashtag = models.SlugField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hashtag

    class Meta:
        verbose_name = _('Hashtag',)
        verbose_name_plural = _('Hashtags',)

class Media(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='media')
    media = models.FileField(
        upload_to='tweets/', max_length=300,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif', 'jpeg', 'mp4'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.media.name

    def clean(self):
        if Media.objects.filter(tweet=self.tweet).count() >= 4 and not self.pk:
            raise ValidationError('tweet can have maximum 4 media')

    def save(self, *args, **kwargs):
        self.clean()
        super(Media, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Media',)
        verbose_name_plural = _('Medias',)


class View(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_views')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='tweet_views')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed {self.tweet}'

    class Meta:
        verbose_name = _('View',)
        verbose_name_plural = _('Views',)


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