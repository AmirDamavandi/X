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


def sign_in(request):
    login_form = LoginForm
    form = login_form()
    context = {'form': form}
    return render(request, 'sign-in/sign-in.html', context)
