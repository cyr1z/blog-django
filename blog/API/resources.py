from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import SAFE_METHODS, IsAdminUser

from blog.API.permissions import ReadOnly, Register
from blog.API.serialisers import PostSerializer, UserSerializer, \
    RegisterSerializer
from blog.models import Post, BlogUser


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [ReadOnly]

    # permission_classes = [IsAdminUser | ReadOnly]
    #
    # def get_serializer_class(self):
    #     if hasattr(self.request, 'method'):
    #         if self.request.method in SAFE_METHODS:
    #             return PostSerializer
    #         elif self.request.method == 'POST':
    #             return CreatePostSerializer
    #         else:
    #             return PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = BlogUser.objects.all()
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAdminUser | Register]

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            if self.request.method in SAFE_METHODS:
                return UserSerializer
            elif self.request.method == 'POST':
                return RegisterSerializer
            else:
                return UserSerializer
