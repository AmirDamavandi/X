from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.views.generic import View
from .models import Tweet
from datetime import datetime

# Create your views here.

class Home(View):
    def get(self, request):
        all_tweets = Tweet.objects.all()
        context = {'tweets': all_tweets}
        return render(request, 'tweets/home/home.html', context)