from django import template

register = template.Library()

@register.simple_tag
def user_like(tweet, user):
    return tweet.user_like(user)