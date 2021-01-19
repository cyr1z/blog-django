from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed


class BlogFeed(Feed):
    title = "blog"
    link = "/posts/"
    description = "RSS feed of blog"

    def items(self):
        return Post.objects.filter(is_published=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text_rendered

    def item_link(self, item):
        return reverse('post_details', args=[item.slug])


class AtomFeed(Feed):
    feed_type = Atom1Feed
