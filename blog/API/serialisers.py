from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'categories', 'tags', 'title', 'text', 'preview', 'created_at', 'published_at', 'is_published', ]