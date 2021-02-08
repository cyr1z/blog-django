from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission, SAFE_METHODS, \
    IsAuthenticated, IsAdminUser

from blog.API.serialisers import PostSerializer
from blog.models import Post


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AuthorizedCreate(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.method == 'POST'


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [ReadOnly]
