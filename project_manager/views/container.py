from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project_manager.models import Container
from project_manager.serializers import ContainerSerializer
from project_manager.permissions import HasContainerAccess
from project_manager.tag_manager import get_by_tag

from .tag_based import TagBasedViewSet


class ContainerViewSet(TagBasedViewSet):

    serializer_class = ContainerSerializer
    permission_classes = [IsAuthenticated,
                          HasContainerAccess]

    @property
    def queryset(self):
        return Container.objects.all()

    def list_children(self, request):
        container = self.get_object()
        children_tag = container.children
        children = [get_by_tag(container.project, tag) for tag in children_tag]
        children_tag = []

        for child in children:
            try:
                self.check_object_permissions(request, child)
            except:
                pass
            else:
                children_tag.append({'tag': child.tag, 'label': child.label})

        return Response(children_tag)


