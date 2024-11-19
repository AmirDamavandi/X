from django.db.transaction import commit
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import media

from .models import *
from django.views.generic import View
from .models import Tweet
from .forms import *
# Create your views here.

class Home(View):
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
        return redirect('tweets:Home')
