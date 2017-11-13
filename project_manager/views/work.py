from django.core.exceptions import PermissionDenied
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from hel.permissions import HasRole

from project_manager.tag_manager import get_by_tag
from project_manager.statuses import *
from project_manager.models import Work, Project
from project_manager.permissions import (
    HasWorkAccess,
    IsExecutor,
    IsVerifier,
)
from project_manager.serializers import (
    MessageSerializer,
    ResourceSerializer,
    WorkSerializer,
)

from .tag_based import TagBasedViewSet


class WorkViewSet(TagBasedViewSet):

    @property
    def queryset(self):
        return Work.objects.all()

    def get_serializer_class(self):
        if self.action == 'post_message':
            return MessageSerializer
        return WorkSerializer

    def get_permissions(self):
        base_permissions = [
            IsAuthenticated,
            HasRole,
            HasWorkAccess,
        ]
        additional_permissions = []

        if self.action in ['start', 'complete']:
            additional_permissions += [IsExecutor]
        elif self.action in ['verify', 'deny']:
            additional_permissions += [IsVerifier]
        elif self.action in ['list_free_cash_workon', 'list_free_cash_available']:
            additional_permissions += [FreeCashAccess]

        self.permission_classes = base_permissions + additional_permissions
        return super().get_permissions()

    def list_free_cash_workon(self, request):
        queryset = self.queryset.filter(Q(executor=request.user)|Q(verifier=request.user))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def list_free_cash_available(self, request):
        queryset = self.queryset.filter((Q(status=STATUS_AWAITING_WORK)&(Q(executor_role=request.user.role)|Q(verifier_role=request.user.role))))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)



    def simple_action(method):
        def wrapper(self, request):
            work = self.get_object()
            try:
                method(self, work)
            except:
                return PermissionDenied()
            return Response({'status': work.status})
        return wrapper

    @simple_action
    def start(self, work):
        work.start()

    @simple_action
    def complete(self, work):
        work.complete()

    @simple_action
    def verify(self, work):
        work.verify()

    @simple_action
    def deny(self, work):
        work.deny()

    @simple_action
    def reactivate(self,work):
        work.reactivate()

    def post_message(self, request):
        work = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, work=work)
        return Response("Success")

