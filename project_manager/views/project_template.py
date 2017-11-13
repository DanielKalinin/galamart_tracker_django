from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (
    ParseError,
    NotFound,
)

from hel.viewsets import ExtendedModelViewSet

from project_manager.tag_manager import get_by_tag
from project_manager.permissions import (
    HasProjectTemplateAccess,
    HasProjectTemplateListAccess,
)
from project_manager.models import ProjectTemplate, Project, Work
from project_manager.access_levels import *
from project_manager.serializers import (
    ProjectTemplateSerializer,
    ContainerTemplateSerializer,
    WorkTemplateSerializer,
    RequirementTemplateSerializer,
    ResourceTemplateSerializer,
    ProjectJSONSerializer,
)


class ProjectTemplateViewSet(ExtendedModelViewSet):

    @property
    def queryset(self):
        return ProjectTemplate.objects.filter(is_template=True)

    def get_serializer_class(self):
        if self.action in ('create', 'list'):
            return ProjectTemplateSerializer
        elif self.action in ('retrieve',):
            return ProjectJSONSerializer

    def get_permissions(self):
        base_permissions = [IsAuthenticated]
        additional_permissions = []

        if self.action in ('update', 'retrieve', 'create'):
            additional_permissions += [HasProjectTemplateAccess]
        elif self.action in ('list',):
            additional_permissions += [HasProjectTemplateListAccess]

        self.permission_classes = base_permissions + additional_permissions
        return super().get_permissions()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            project.participants.add(request.user)
            return Response({"id": project.id})

    def update(self, request):
        project = ProjectTemplate.updateFromJSON(request.data)
        return Response("Success")

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request):
        if not 'id' in request.query_params:
            raise ParseError("Field 'id' should be in query params")
        try:
            project = self.queryset.get(pk=request.query_params['id'])
        except ProjectTemplate.DoesNotExist:
            raise NotFound("Project template with this 'id' does not exist")

        serializer = self.get_serializer(project)
        return Response(serializer.data)



class StageViewSet(ExtendedModelViewSet):

    def add_stage(self, request, pk):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = self.get_object()

            stage = serializer.save(project=project)

            project.children.append(stage.tag)
            project.save()
            return Response("Success")  # TODO: CHECK WHETHER TAG IS CORRECT

    def stage_detail(self, request, pk, stage_tag):
        project = self.get_object()
        try:
            stage = get_by_tag(project, stage_tag)
        except:
            return Response("Incorrect stage tag")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(stage)
        return Response(serializer.data)

    def add_desk(self, request, pk, stage_tag):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = self.get_object()

            try:
                stage = get_by_tag(project, stage_tag)
            except:
                return Response("Incorrect stage tag")

            desk = serializer.save(project=project)

            stage.children.append(desk.tag)
            stage.save()

            return Response("Success")

    def desk_detail(self, request, pk, desk_tag):
        project = self.get_object()
        try:
            desk = get_by_tag(project, desk_tag)
        except:
            return Response("Incorrect desk tag")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(desk)
        return Response(serializer.data)

    def add_work(self, request, pk, desk_tag):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = self.get_object()

            try:
                desk = get_by_tag(project, desk_tag)
            except:
                return Response("Incorrect desk tag")

            work = serializer.save(project=project)  # TODO: Think about related field for works - desk

            desk.children.append(work.tag)
            desk.save()

            return Response("Success")

    def work_detail(self, request, pk, work_tag):
        project = self.get_object()
        try:
            work = get_by_tag(project, work_tag)
        except:
            return Response("Incorrect work tag")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(work)
        return Response(serializer.data)

    def add_requirement(self, request, pk, work_tag):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = self.get_object()

            try:
                work = get_by_tag(project, work_tag)
            except:
                return Response("Incorrect work tag")

            requirement = serializer.save(project=project)

            work.requirements.append(requirement.tag)
            work.save()

            return Response("Success")

    def requirement_detail(self, request, pk, requirement_tag):
        project = self.get_object()
        try:
            requirement = get_by_tag(project, requirement_tag)
        except:
            return Response("Incorrect requirement tag")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(requirement)
        return Response(serializer.data)

    def add_resource(self, request, pk, work_tag):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = self.get_object()
            try:
                work = get_by_tag(project, work_tag)
            except:
                return Response("Incorrect work tag")

            resource = serializer.save(project=project)

            work.resources.append(resource.tag)
            work.save()

            return Response("Success")

    def resource_detail(self, request, pk, resource_tag):
        project = self.get_object()
        try:
            resource = get_by_tag(project, resource_tag)
        except:
            return Response("Incorrect resource tag")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(resource)
        return Response(serializer.data)

