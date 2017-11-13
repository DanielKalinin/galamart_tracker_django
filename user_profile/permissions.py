from rest_framework import permissions


class IsNotCreationOrIsNotAuthorized(permissions.BasePermission):

    def has_permission(self, request, view):
        creation_views = ('create', 'confirm')
        if view.action not in creation_views:
            return True
        else:
            return not request.user or not request.user.is_authenticated()

