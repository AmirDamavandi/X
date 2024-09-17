from django.shortcuts import render
from .forms import *
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
# Create your views here.


class X(View):
    template_name = 'x_page/x.html'

    def get(self, request):
        return render(request, self.template_name)


class SignUpView(View):
    template_name = 'sign-up/sign-up.html'
    form = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('you don\' need to sign up, you authenticated already')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        signup_form = self.form()
        context = {'form': signup_form}
        return render(request, self.template_name, context)

    def post(self, request):
        signup_form = self.form(request.POST)
        if signup_form.is_valid():
            cd = signup_form.cleaned_data
            user = User(
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                username=cd['username'],
                email=cd['email'],
                phone_number=cd['phone_number'],
                password=cd['password1'],
            )
            user.set_password(cd['password1'])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse('you are now logged in')
        return render(request, self.template_name, {'form': signup_form})


class LoginView(View):
    template_name = 'login/login.html'
    login_form = LoginForm

    def get(self, request):
        form = self.login_form()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.login_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('logged in')
        return render(request, self.template_name, {'form': form})