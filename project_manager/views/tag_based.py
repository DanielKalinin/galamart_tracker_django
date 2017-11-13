from django.http import Http404

from rest_framework.exceptions import ParseError, NotFound

from hel.viewsets import ExtendedModelViewSet

from project_manager.tag_manager import get_by_tag
from project_manager.models import Project


class TagBasedViewSet(ExtendedModelViewSet):

    def get_tag_object_from_query(self, request, primary=False, field='tag', project_field='project_id'):
        params = request.data if request.method == 'POST' else request.query_params
        try:
            tag = params[field]
        except KeyError:
            raise ParseError("Field '{}' should be in query params or in post data".format(field))
        try:
            project_id = params[project_field]
        except KeyError:
            raise ParseError("Field '{}' should be in query params or in post data".format(project_field))

        if request.method == 'POST':
            request.data.pop(field) and request.data.pop(project_field)

        try:
            project = Project.objects.get(is_template=False, id=project_id)
        except Project.DoesNotExist:
            raise NotFound("Project with this id doesn't exist")

        try:
            obj = get_by_tag(project, tag)
        except:
            raise NotFound("Object with this tag doesn't exist")

        if primary:
            self.check_object_permissions(self.request, obj)
        return obj

    def get_object(self):
        return self.get_tag_object_from_query(
            self.request,
            primary=True,
            field='tag',
            project_field='project_id',
        )

