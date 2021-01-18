from django import template

from blog.models import Category, Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.filter(is_active=True).count()


@register.inclusion_tag('top_nav.html')
def show_top_navigate():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('most_popular_posts.html')
def show_most_popular_posts(count=5):
    most_popular_posts = Post.objects.all().order_by('-views')[0:count]
    return {'most_popular_posts': most_popular_posts}
