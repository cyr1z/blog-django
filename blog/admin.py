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
admin.site.register(BlogUser)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    list_display = ('title', 'thumb')
    list_filter = ('created_at',)

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
    list_display = ('alt', 'album')
    list_filter = ('album',)


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
