import math
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from unidecode import unidecode
from autoslug import AutoSlugField
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe

from blog_with_rest.settings import READ_SPEED, AVATAR_TEMPLATE, \
    DEFAULT_AVATAR, DEFAULT_POST_IMAGE
from django.urls import reverse
from bs4 import BeautifulSoup
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    site_name = models.CharField(max_length=40, default='My blog')
    support = models.EmailField(default='support@example.com')
    contact_email = models.EmailField(default='support@example.com')
    contact_tg = models.CharField(max_length=255, null=True, blank=True)
    contact_tg_id = models.CharField(max_length=255, null=True, blank=True)
    support_tg = models.CharField(max_length=255, null=True, blank=True)
    support_tg_id = models.CharField(max_length=255, null=True, blank=True)

    contact_about_text = RichTextUploadingField(null=True, blank=True)
    fb_link = models.CharField(max_length=255, null=True, blank=True)
    tg_link = models.CharField(max_length=255, null=True, blank=True)
    youtube_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    github_link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'


class BlogUser(AbstractUser):
    """
    Customised Django User Model
    Add avatar, telegram name and telegram id
    unique combinations of First Name and Last Name
    """
    avatar_image = models.ImageField(
        verbose_name='Image',
        upload_to='users_images/',
        null=True,
        blank=True
    )
    about = models.TextField(
        max_length=100000,
        null=True,
        blank=True
    )
    tg_name = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )
    tg_id = models.CharField(
        max_length=120,
        null=True,
        blank=True
    )
    social_picture = models.TextField(blank=True, null=True)

    slug = AutoSlugField(populate_from='username')

    @property
    def full_name(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.username

    @property
    def avatar(self):
        avatar_url = DEFAULT_AVATAR
        if self.social_picture:
            avatar_url = self.social_picture
        else:
            try:
                avatar_url = self.avatar_image.url
            except ValueError:
                pass
        return mark_safe(AVATAR_TEMPLATE.format(avatar_url, self.full_name))

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.get_username()} / {self.get_full_name()}'


class Category(models.Model):
    """
    Category
    """
    title = models.CharField(
        max_length=120
    )
    description = models.TextField(
        max_length=100000,
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name='Image',
        upload_to='categories_images/',
        default='static/category.png',
        null=True,
        blank=True
    )
    is_published = models.BooleanField(
        default=True
    )

    @property
    def unicode_title(self):
        return unidecode(self.title)

    slug = AutoSlugField(populate_from='unicode_title')

    @property
    def posts(self):
        return self.category_posts

    def get_absolute_url(self):
        return reverse('categories', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    """
    Tags
    """
    title = models.CharField(
        max_length=120
    )

    @property
    def unicode_title(self):
        return unidecode(self.title)

    slug = AutoSlugField(populate_from='unicode_title')

    def get_absolute_url(self):
        return reverse('tags', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class Post(models.Model):
    """
    Post
    """
    user = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_posts'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='category_posts'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag_posts',
        blank=True,
    )
    title = models.CharField(
        max_length=120
    )

    text = RichTextUploadingField(null=True, blank=True, )

    @property
    def clean_text(self):
        return BeautifulSoup(
            self.text, features="html.parser").get_text().strip()

    @property
    def short_text(self):
        clean_text = self.clean_text
        d = clean_text[200:]
        t = d.split('.')
        return clean_text[:200] + t[0] + '...'

    preview = models.ImageField(
        verbose_name='Image',
        upload_to='posts_images/',
        default=DEFAULT_POST_IMAGE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    published_at = models.DateTimeField(
        default=timezone.now
    )
    is_published = models.BooleanField(
        default=True
    )

    minutes_to_read = models.IntegerField(
        default=0
    )

    @property
    def unicode_title(self):
        return unidecode(self.title)

    slug = AutoSlugField(populate_from='unicode_title')

    views = models.PositiveIntegerField(
        default=0
    )

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.minutes_to_read:
            self.minutes_to_read = math.ceil(len(self.text) / READ_SPEED)
        super().save(*args, **kwargs)

    pinned_on_main_top = models.BooleanField(
        default=False
    )
    pinned_on_main_bottom = models.BooleanField(
        default=False
    )

    @property
    def category_links(self):
        result = ''
        for num, c in enumerate(self.categories.all()):
            if num:
                result += ', '
            result += '<a href="' \
                      + reverse('category_details', args=[c.slug]) \
                      + f'">{c.title}</a>'
        return result

    @property
    def tags_links(self):
        result = ''
        for num, c in enumerate(self.tags.all()):
            if num:
                result += ', '
            result += '<a href="' \
                      + reverse('tag_details', args=[c.slug]) \
                      + f'">#{c.title}</a>'
        return result

    def increment_view_count(self):
        self.views += 1
        self.save()

    def __str__(self):
        return f'{self.title} / Author: {self.user.full_name} ' \
               f'/ Created: {self.created_at} / ' \
               f'categories: ' \
               f'{", ".join([x.title for x in self.categories.all()])}'


class Comment(models.Model):
    """
    Comment
    """
    user = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        related_name='post_comments'
    )
    # parent = models.ForeignKey(
    #     'blog.Comment',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     related_name='comment_comments'
    # )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    text = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="text",
    )
    updated = models.DateTimeField(
        default=timezone.now
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Post Comments'

    def __str__(self):
        return f'{self.user.full_name} to {self.post.title}: {self.text}'

    def deactivate(self):
        self.active = False
        self.save()


class Album(models.Model):
    title = models.CharField(max_length=70)
    thumb = ProcessedImageField(
        upload_to='albums',
        processors=[ResizeToFit(300)],
        format='JPEG',
        options={'quality': 90}
    )
    post = models.OneToOneField(
        Post,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='album'

    )
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def unicode_title(self):
        return unidecode(self.title)

    slug = AutoSlugField(populate_from='unicode_title')

    def __str__(self):
        return self.title


class AlbumImage(models.Model):
    image = ProcessedImageField(
        upload_to='albums',
        processors=[ResizeToFit(1280)],
        format='JPEG',
        options={'quality': 70}
    )
    thumb = ProcessedImageField(
        upload_to='albums',
        processors=[ResizeToFit(300)],
        format='JPEG',
        options={'quality': 80}
    )
    album = models.ForeignKey(Album, on_delete=models.PROTECT,
                              related_name='album_images')
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)
