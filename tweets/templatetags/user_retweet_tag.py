from django import template

register = template.Library()

@register.simple_tag
def user_retweet(tweet, user):
    return tweet.user_retweet(user)