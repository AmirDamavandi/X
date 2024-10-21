from .models import *
import random
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def active_user(request):
    context = {'active_user': request.user}
    return context

def suggest_to_follow(request):
    if not request.user.is_authenticated:
        return {}
    authenticated_user = request.user
    followers = None
    authenticated_user_followings = []
    if User.following_count(authenticated_user) >= 3:
        followers = Relation.objects.filter(from_user=authenticated_user)
        for relation in range(3):
            random_user = random.choice(followers)
            following = random_user.to_user.username
            user = User.objects.get(username=following)
            if not user in authenticated_user_followings:
                authenticated_user_followings.append(user)

    user_count = 0
    suggesting_to_follow = []
    for user in authenticated_user_followings:
        user_count += 1
        following_followers = Relation.objects.filter(from_user=user)
        if following_followers.count() > 0:
            random_following_followers = random.choice(following_followers)
            users = random_following_followers.to_user.username
            suggestions = User.objects.get(username=users)
            suggesting_to_follow.append(suggestions)
        if user_count == 3:
            break
    suggestions = []
    if suggesting_to_follow:
        for user in suggesting_to_follow:
            query = Relation.objects.filter(from_user=authenticated_user, to_user=user)
            if not query:
                suggestions.append(user)
    for user in suggestions:
        query = ConnectPeople.objects.filter(user=request.user, linked_user=user)
        query_count = ConnectPeople.objects.filter(user=authenticated_user).count()
        if not query and not query_count >= 5 and not user == authenticated_user:
            link_people = ConnectPeople(
                user=request.user, linked_user=user, link_reason='followed by their followings'
            )
            link_people.save()
    suggest_people = []
    for user in range(3):
        people = ConnectPeople.objects.filter(user=authenticated_user)
        if people.count() > 0:
            random_people = random.choice(people)
            users = random_people.linked_user.username
            check_user = User.objects.get(username=users)
            following_check = Relation.objects.filter(from_user=authenticated_user, to_user__username=users)
            if following_check.exists():
                get_connection = ConnectPeople.objects.get(user=request.user, linked_user__username=users)
                get_connection.delete()
            if not check_user in suggest_people:
                suggest_people.append(check_user)
    if Relation.objects.filter(from_user=authenticated_user).count() < 3:
        people = []
        for user in range(3):
            users = User.objects.all()
            random_people = random.choice(users)
            if not random_people in people:
                people.append(random_people)
        context = {'users': people}
        return context

    context = {'users': suggest_people}
    return context

