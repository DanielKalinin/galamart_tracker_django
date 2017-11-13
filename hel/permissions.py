from rest_framework import permissions


class IsAuthorized(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()


class HasRole(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role

