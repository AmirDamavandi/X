from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import *
from .context_processor import suggest_to_follow, active_user
# Create your views here.


class X(View):
    template_name = 'x_page/x.html'

    def get(self, request):
        print(self.request.user)
        return render(request, self.template_name)


class SignUpView(View):
    template_name = 'sign-up/sign-up.html'
    form = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('you don\' need to sign up, you authenticated already')
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        signup_form = self.form()
        context = {'form': signup_form}
        return render(request, self.template_name, context)

    def post(self, request):
        signup_form = self.form(request.POST)
        if signup_form.is_valid():
            cd = signup_form.cleaned_data
            user = User.objects.create_user(
                first_name=cd['first_name'],
                username=cd['username'],
                email=cd['email'],
                password=cd['password1']
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse('you are now logged in')
        return render(request, self.template_name, {'form': signup_form})


class LoginView(View):
    template_name = 'login/login.html'
    login_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('you are already logged in')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.login_form()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.login_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('accounts:ProfileView', user.username)
        return render(request, self.template_name, {'form': form})


class ProfileView(View):
    template_name = 'profile/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:LoginView')
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if user.is_authenticated and user.following_check(self.request.user):
            following = True
        else:
            following = False
        context = {'user': user, 'following': following}
        return render(request, self.template_name, context)


class FollowView(View):

    def post(self, request, username):
        query = Relation.objects.filter(from_user__username=self.request.user, to_user__username=username)
        following_user = User.objects.get(username=username)
        if not query.exists():
            follow = Relation(from_user=self.request.user, to_user=following_user)
            follow.save()
        return redirect('accounts:ProfileView', username)


class UnfollowView(View):

    def post(self, request, username):
        unfollowing_user = User.objects.get(username=username)
        query = Relation.objects.filter(from_user=self.request.user, to_user=unfollowing_user)
        if query.exists():
            unfollow = Relation.objects.get(from_user=self.request.user, to_user=unfollowing_user)
            unfollow.delete()
        return redirect('accounts:ProfileView', username)
