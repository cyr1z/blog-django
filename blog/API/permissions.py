from rest_framework.permissions import BasePermission, SAFE_METHODS


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

