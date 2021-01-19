"""blog_with_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from blog.models import Post
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from blog.sitemaps import StaticViewSitemap
from blog.feeds import BlogFeed

sitemaps = {
    'blog': GenericSitemap({
        'queryset': Post.objects.all(),
        'date_field': 'published_at',
    }, priority=0.9),
    # 'static': StaticViewSitemap,
}

urlpatterns = [
    path('', include('blog.urls')),
    path('sitemap.xml', sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path("feed/", BlogFeed(), name="feed"),
    path('admin/', admin.site.urls),

]
