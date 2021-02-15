import os
import uuid
from zipfile import ZipFile
from django.contrib import admin
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
from PIL import Image
from blog_with_rest.settings import MEDIA_ROOT
from .forms import AlbumForm
from .models import Category, BlogUser, Tag, Post, Comment, Album, AlbumImage, \
    SiteSettings

#
# class ProductAdmin(admin.ModelAdmin):
#     readonly_fields = ["preview"]
#
#     def preview(self, obj):
#         return mark_safe(f'<img src="{obj.image.url}" height="200">')


admin.site.register(Category)

admin.site.register(Tag)
admin.site.register(Comment)


@admin.register(BlogUser)
class AdminModelUser(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_staff', 'is_active',
                    'get_preview')
    readonly_fields = ("get_image",)
    actions = ["deactivate", "activate"]

    def get_preview(self, obj):
        return mark_safe(
            f'<div style="height: 42px; display: block; box-sizing: border-box;"'
            f'>{obj.avatar}</div>')

    def get_image(self, obj):
        return mark_safe(
            f'<div style="height: 160px; display: block; box-sizing: border-box;"'
            f'>{obj.avatar}</div>')

    def deactivate(self, request, queryset):
        """deactivate users"""
        row_update = queryset.update(is_active=False)
        if row_update == 1:
            message_bit = "1 user deactivated"
        else:
            message_bit = f"{row_update} users deactivated"
        self.message_user(request, f"{message_bit}")

    def activate(self, request, queryset):
        """activate users"""
        row_update = queryset.update(is_active=True)
        if row_update == 1:
            message_bit = "1 user activated"
        else:
            message_bit = f"{row_update} users activated"
        self.message_user(request, f"{message_bit}")

    activate.short_description = "activate"
    activate.allowed_permissions = ('change',)
    deactivate.short_description = "deactivate"
    deactivate.allowed_permissions = ('change',)

    get_preview.short_description = "Avatar"
    get_image.short_description = "Avatar"


@admin.register(Post)
class AdminModelPost(admin.ModelAdmin):
    list_display = (
    'title', 'get_preview', 'user', 'created_at', 'is_published')
    list_filter = ('created_at', 'user')
    readonly_fields = ("get_image",)
    actions = ["publish", "unpublish"]

    def get_preview(self, obj):
        return mark_safe(f'<img src={obj.preview.url} style="'
                         f'border: 1px solid #ddd;  border-radius: 3px;'
                         f'padding: 5px; max-width: 60px; max-height: 60"')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.preview.url} style="'
                         f'border: 1px solid #ddd;  border-radius: 3px;'
                         f'padding: 5px; max-width: 160px; max-height: 160"')

    def unpublish(self, request, queryset):
        """Unpublish"""
        row_update = queryset.update(is_published=False)
        if row_update == 1:
            message_bit = "1 post updated"
        else:
            message_bit = f"{row_update} posts updated"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Post"""
        row_update = queryset.update(is_published=True)
        if row_update == 1:
            message_bit = "1 post updated"
        else:
            message_bit = f"{row_update} posts updated"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "publish"
    publish.allowed_permissions = ('change',)
    unpublish.short_description = "unpublish"
    unpublish.allowed_permissions = ('change',)

    get_preview.short_description = "Image"
    get_image.short_description = "Image"


class ImagesInline(admin.StackedInline):
    model = AlbumImage
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    list_display = ('title', 'get_preview')
    list_filter = ('created_at',)
    readonly_fields = ("get_preview",)
    inlines = [ImagesInline, ]

    def get_preview(self, obj):
        return mark_safe(f'<img src={obj.thumb.url} style="'
                         f'border: 1px solid #ddd;  border-radius: 3px;'
                         f'padding: 5px; max-width: 160px; max-height: 160px"')

    get_preview.short_description = "Image"

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            album = form.save(commit=False)
            album.save()

            if form.cleaned_data['zip']:
                zip_file = ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip_file.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = zip_file.read(filename)
                    content_file = ContentFile(data)

                    img = AlbumImage()
                    img.album = album
                    img.alt = filename
                    filename = f'{album.slug}{str(uuid.uuid4())[-13:]}.jpg'
                    img.image.save(filename, content_file)

                    filepath = f'{MEDIA_ROOT}/albums/{filename}'
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    img.thumb.save(f'thumb-{filename}', content_file)
                    img.save()
                zip_file.close()
            super(AlbumModelAdmin, self).save_model(request, obj, form, change)


@admin.register(AlbumImage)
class AlbumImageModelAdmin(admin.ModelAdmin):
    list_display = ('alt', 'album', 'get_preview')
    list_filter = ('album',)
    readonly_fields = ("get_image",)

    def get_preview(self, obj):
        return mark_safe(f'<img src={obj.image.url} style="'
                         f'border: 1px solid #ddd;  border-radius: 3px;'
                         f'padding: 5px; max-width: 60px; max-height: 60"')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} style="'
                         f'border: 1px solid #ddd;  border-radius: 3px;'
                         f'padding: 5px; max-width: 160px; max-height: 160"')

    get_preview.short_description = "Image"


class SingletonModelAdmin(admin.ModelAdmin):
    """
    Prevents Django admin users deleting the singleton or adding extra rows.
    """
    actions = None  # Removes the default delete action.

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    pass
