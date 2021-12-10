from ..models import Post
from django import template
from django.db.models import Count

register = template.Library()
# @register.simple_tag(name=rcpcount_tag) - specifying tag name
# use post_list view to create inclusion tag for home page

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('recipes/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    context = {'latest_posts': latest_posts}
    return context


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

