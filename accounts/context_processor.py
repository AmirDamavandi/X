from .models import *


def active_user(request):
    context = {'active_user': request.user}
    return context