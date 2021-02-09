from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission, SAFE_METHODS, \
    IsAuthenticated, IsAdminUser

from blog.API.serialisers import PostSerializer, UserSerializer, \
    RegisterSerializer
from blog.models import Post, BlogUser


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AuthorizedCreate(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.method == 'POST'


class Register(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method == 'POST'


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [ReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = BlogUser.objects.all()
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAdminUser | Register]

    def get_serializer_class(self):
        print(self.request.method)
        if hasattr(self.request, 'method'):
            if self.request.method in SAFE_METHODS:
                return UserSerializer
            elif self.request.method == 'POST':
                return RegisterSerializer
            else:
                return UserSerializer
