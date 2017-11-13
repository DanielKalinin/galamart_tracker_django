from functools import wraps
from rest_framework import permissions

from project_manager.access_levels import *
from project_manager.models import Work


def access_from_list(user, access_level):
    if not access_level in ACCESS_LIST[user.role]:
        return False
    return True


def require_auth(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user:
            return False
        return func(self, request, *args, **kwargs)
    return wrapper

class IsExecutor(permissions.BasePermission):

    @require_auth
    def has_object_permission(self, request, view, obj):
        return request.user == obj.executor


class IsVerifier(permissions.BasePermission):

    @require_auth
    def has_object_permission(self, request, view, obj):
        return request.user == obj.verifier


class HasWorkAccess(permissions.BasePermission):

    @require_auth
    def has_object_permission(self, request, view, obj):
        return access_from_list(request.user, SEE_SELF_PROJECT) and \
            request.user in obj.project.participants.all() or \
            obj.is_available() and obj.has_access(request.user)


class HasContainerAccess(permissions.BasePermission):

    @require_auth
    def has_object_permission(self, request, view, obj):
        return access_from_list(request.user, SEE_SELF_PROJECT) and \
            request.user in obj.project.participants.all() or \
            obj.is_available() and obj.has_access(request.user)


class HasResourceAccess(permissions.BasePermission):

    @require_auth
    def has_object_permission(self, request, view, obj):
        works = Work.objects.filter(resources__contains=[obj.tag])
        for work in works:
            if work.is_available() and work.has_access(request.user):
                return True
        return False


class HasProjectAccess(permissions.BasePermission):

    @require_auth
    def has_object_permission(self, request, view, obj):
        return access_from_list(request.user, SEE_ANY_PROJECT) or\
            access_from_list(request.user, SEE_SELF_PROJECT) and request.user in obj.participants.all()


class HasProjectCreationAccess(permissions.BasePermission):

    @require_auth
    def has_permission(self, request, view):
        return access_from_list(request.user, CREATE_GALA_PROJECT) or\
            access_from_list(request.user, CREATE_FRANCH_PROJECT)


class HasProjectTemplateAccess(permissions.BasePermission):

    @require_auth
    def has_permission(self, request, view):
        return access_from_list(request.user, CHANGE_WORKFLOW)


class HasProjectTemplateListAccess(permissions.BasePermission):

    @require_auth
    def has_permission(self, request, view):
        return access_from_list(request.user, CHANGE_WORKFLOW) or\
            access_from_list(request.user, CREATE_GALA_PROJECT) or\
            access_from_list(request.user, CREATE_FRANCH_PROJECT)


class FreeCashAccess(permissions.BasePermission):

    @require_auth
    def has_permission(self, request, view):
        return access_from_list(request.user, FREE_CASH)

