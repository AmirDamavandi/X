from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from .forms import *
from django.template.loader import render_to_string
# Create your views here.

class Home(LoginRequiredMixin, View):
    def get(self, request):
        tweet_form = TweetModelForm()
        media_form = MediaFormSet()
        all_tweets = Tweet.objects.all().order_by('-created_at')
        context = {
            'tweets': all_tweets,
            'tweet_form': tweet_form,
            'media_form': media_form,
        }
        return render(request, 'tweets/home/home.html', context)

    def post(self, request):
        tweet_form = TweetModelForm(request.POST)
        if tweet_form.is_valid():
            user = request.user
            tweet = Tweet(user=user, **tweet_form.cleaned_data)
            tweet.user = request.user
            tweet.save()
            media_form = MediaFormSet(request.POST, request.FILES, instance=tweet)
            if media_form.is_valid():
                media_form.save()
            rendered_tweet = render_to_string('base/tweets/new_tweet.html', {'tweet': tweet})
            return JsonResponse({
                'status': 'ok',
                'rendered_tweet': rendered_tweet,
            })
        return JsonResponse(
            {'status': 'error', 'rendered_tweet': tweet_form.errors}
        )

class LikeTweetView(View):
    def post(self, request, tweet_id):
        is_liked = False
        user = request.user
        tweet = Tweet.objects.get(pk=tweet_id)
        liked_before = Like.objects.filter(user=user, tweet=tweet).exists()
        if not liked_before:
            new_like = Like(user=user, tweet_id=tweet_id)
            new_like.save()
            is_liked = True
        return JsonResponse(
            {'is_liked': is_liked}
        )


class UnLikeTweetView(View):
    def post(self, request, tweet_id):
        unliked = False
        user = request.user
        tweet = Tweet.objects.get(pk=tweet_id)
        liked_before = Like.objects.filter(user=user, tweet=tweet).exists()
        if liked_before:
            dislike = Like.objects.get(user=user, tweet_id=tweet_id)
            dislike.delete()
            unliked = True
        return JsonResponse(
            {'unliked': unliked}
        )


class RetweetView(View):
    def post(self, request, tweet_id):
        retweeted = False
        user = request.user
        tweet = Tweet.objects.get(pk=tweet_id)
        retweeted_before = Retweet.objects.filter(user=user, tweet=tweet).exists()
        if not retweeted_before:
            new_retweet = Retweet(user=user, tweet=tweet)
            new_retweet.save()
            retweeted = True
        return JsonResponse(
            {'retweeted': retweeted}
        )

class UndoRetweetView(View):
    def post(self, request, tweet_id):
        unretweeted = False
        user = request.user
        tweet = Tweet.objects.get(pk=tweet_id)
        retweeted_before = Retweet.objects.filter(user=user, tweet=tweet).exists()
        if retweeted_before:
            retweet = Retweet.objects.get(user=user, tweet_id=tweet_id)
            retweet.delete()
            unretweeted = True
        return JsonResponse(
            {'unretweeted': unretweeted}
        )