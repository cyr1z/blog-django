import markdown
from django import template
from django.utils.safestring import mark_safe

from blog.models import Category, Post, SiteSettings

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.filter(is_published=True).count()


@register.inclusion_tag('top_nav.html')
def show_top_navigate():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('most_popular_posts.html')
def show_most_popular_posts(count=5):
    most_popular_posts = Post.objects.filter(is_published=True).order_by('-views')[0:count]
    return {'most_popular_posts': most_popular_posts}


@register.inclusion_tag('site_logo_name.html')
def show_logo_name():
    return {'name': SiteSettings.objects.first().site_name}


@register.inclusion_tag('about_us_in_contact.html')
def show_contact_about():
    return {'about_text': SiteSettings.objects.first().contact_about_text}


@register.inclusion_tag('top_social_icons.html')
def show_top_social():
    socials = {
        'fb_link': SiteSettings.objects.first().fb_link,
        'tg_link': SiteSettings.objects.first().tg_link,
        'youtube_link': SiteSettings.objects.first().youtube_link,
        'twitter_link': SiteSettings.objects.first().twitter_link,
        'instagram_link': SiteSettings.objects.first().instagram_link,
        'github_link': SiteSettings.objects.first().github_link,

    }
    return socials


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
