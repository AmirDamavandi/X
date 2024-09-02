from django.shortcuts import render
from .forms import *
# Create your views here.


def x(request):
    return render(request, 'x_page/x.html')


def sign_up(request):
    signup_form = SignupForm
    form = signup_form()
    context = {'form': form}
    return render(request, 'sign-up/sign-up.html', context)
