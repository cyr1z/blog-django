from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from .models import Category, BlogUser, Tag, Post, Content, Comment


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="200">')


admin.site.register(Category)
admin.site.register(BlogUser)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Content)
admin.site.register(Comment)
