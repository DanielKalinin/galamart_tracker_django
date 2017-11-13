from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError

from hel.permissions import HasRole
from hel.viewsets import ExtendedModelViewSet

from project_manager.models import Project, ProjectTemplate
from project_manager.serializers import ProjectSerializer
from project_manager.access_levels import *
from project_manager.permissions import (
    HasProjectAccess,
    IsExecutor,
    HasProjectCreationAccess,
)


class ProjectViewSet(ExtendedModelViewSet):

    serializer_class = ProjectSerializer

    @property
    def queryset(self):
        return Project.objects.filter(is_template=False)

    def get_permissions(self):
        base_permissions = [
            IsAuthenticated,
            HasRole,
            HasProjectAccess,
        ]
        additional_permissions = []

        if self.action == 'create':
            additional_permissions += [HasProjectCreationAccess]

        self.permission_classes = base_permissions + additional_permissions
        return super().get_permissions()

    def retrieve(self, request):
        project = self.get_object()
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def list(self, request):
        queryset = self.queryset.filter(is_template=False, participants__id=request.user.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if not 'template_id' in request.data:
            raise ParseError("Field 'template_id' is required'")
        data = { key: value for key, value in request.data.items() if key != 'template_id' }

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save(request=request, template_id=request.data['template_id'])
            project.open()
            return Response({"id": project.id})

    def update(self, request):
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            return Response("Updated")

