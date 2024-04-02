from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('core/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts} # inclusion_tag has to return dictionary.


@register.simple_tag
def get_most_commented_posts(count=5):
    """
    Accept count parameter and return the most commemted post limits by the given count
    """
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]