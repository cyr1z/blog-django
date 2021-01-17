import math

from autoslug import AutoSlugField
from django.db.models import F
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from blog_with_rest.settings import READ_SPEED
from django.core.exceptions import ValidationError
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from django.urls import reverse


class BlogUser(AbstractUser):
    """
    Customised Django User Model
    Add avatar, telegram name and telegram id
    unique combinations of First Name and Last Name
    """
    avatar_image = models.ImageField(
        verbose_name='Image',
        upload_to='static/users_images',
        default='avatar.png',
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

    slug = AutoSlugField(populate_from='username')

    @property
    def full_name(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.username

    @property
    def avatar(self):
        img_url = self.avatar_image.url
        img_string = f'<img src="{img_url}" alt="{self.full_name}">'
        return mark_safe(img_string)

    class Meta:
        # unique_together = ["first_name", "last_name"]
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
        upload_to='static/categories_images',
        default='static/category.png',
        null=True,
        blank=True
    )
    is_published = models.BooleanField(
        default=True
    )

    slug = AutoSlugField(populate_from='title')

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

    slug = AutoSlugField(populate_from='title')

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
    )
    title = models.CharField(
        max_length=120
    )
    text = MarkdownField(
        rendered_field='text_rendered',
        validator=VALIDATOR_STANDARD
    )

    @property
    def short_text(self):
        d = self.text[200:]
        t = d.split('.')
        return self.text[:200] + t[0] + '...'

    text_rendered = RenderedMarkdownField()
    preview = models.ImageField(
        verbose_name='Image',
        upload_to='static/posts_images',
        default='static/post.png',
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

    slug = AutoSlugField(populate_from='title')

    views = models.PositiveIntegerField(
        default=0
    )

    def get_absolute_url(self):
        return reverse('posts', kwargs={'slug': self.slug})

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

    # the field name should be comments
    # comments = GenericRelation(Comment)

    def __str__(self):
        return f'{self.title} / Author: {self.user.full_name} ' \
               f'/ Created: {self.created_at} / ' \
               f'categories: ' \
               f'{", ".join([x.title for x in self.categories.all()])}'


class Content(models.Model):
    """
    Additional pictures, audio or video content
    """

    class ContentTypes(models.TextChoices):
        VIDEO = 'video'
        AUDIO = 'audio',
        IMAGE = 'image'
        # LINK = 'link',
        # MAP = 'map',

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        related_name='post_contents'
    )
    type = models.CharField(
        max_length=5,
        choices=ContentTypes.choices,
        default=ContentTypes.IMAGE,
    )
    image = models.ImageField(
        verbose_name='Image',
        upload_to='static/contents_files',
        null=True,
        blank=True
    )
    file = models.FileField(
        upload_to='static/contents_files',
    )
    link = models.URLField(
        max_length=800
    )

    def save(self, *args, **kwargs):
        if self.image and self.file or self.file and self.link \
                or self.link and self.image:
            raise ValidationError('Not one content element')
        super().save(*args, **kwargs)


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
