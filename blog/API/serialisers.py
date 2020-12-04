from rest_framework import serializers

from blog.models import Post, BlogUser, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ['avatar_image', 'about', 'tg_name', 'tg_id', 'username',
                  'first_name', 'last_name', 'email', 'id', ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug', ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'description', 'image', 'is_published', 'slug', ]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['user', 'categories', 'tags', 'title', 'text', 'preview',
                  'created_at', 'published_at', 'is_published', 'slug', ]

