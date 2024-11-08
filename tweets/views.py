from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.views.generic import View
# Create your views here.


class Hashtags(View):
    def get(self, request):
        hashtags = Hashtag.objects.all()
        hashtag_count = 0
        print(hashtag_count)
        return HttpResponse('printing hashtags')