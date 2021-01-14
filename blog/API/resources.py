from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication

from blog.API.serialisers import PostSerializer
from blog.models import Post


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [BasicAuthentication, ]
