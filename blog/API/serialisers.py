from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from blog.models import Post, BlogUser, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ['avatar_image', 'about', 'tg_name', 'tg_id', 'username',
                  'first_name', 'last_name', 'email', 'id',
        ]


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
        fields = ['user', 'categories', 'tags', 'title', 'text',
                  'clean_text', 'preview',
                  'created_at', 'published_at', 'is_published', 'slug', ]




class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=BlogUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BlogUser
        fields = ('username', 'password', 'password2', 'email', 'first_name',
                  'last_name', 'about', 'tg_name', 'tg_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = BlogUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            tg_name=validated_data['tg_name'],
            tg_id=validated_data['tg_id'],
            about=validated_data['about'],

        )

        user.set_password(validated_data['password'])
        user.save()

        return user
