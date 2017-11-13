from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from project_manager.serializers import (
    ResourceSerializer,
    ResourceFileDataSerializer,
)
from project_manager.models import Resource
from project_manager.permissions import (
    HasResourceAccess,
)
from project_manager.resource_types import *

from .tag_based import TagBasedViewSet

class ResourceViewSet(TagBasedViewSet):

    permission_classes = [
        IsAuthenticated,
        #HasResourceAccess
    ]
    serializer_class = ResourceSerializer

    @property
    def queryset(self):
        return Resource.objects.all()


class ResourceFileViewSet(TagBasedViewSet):

    parser_classes = (MultiPartParser,)
    serializer_class = ResourceFileDataSerializer
    permission_classes = [
        IsAuthenticated,
        #HasResourceAccess,
    ]

    @property
    def queryset(self):
        return Resource.objects.all()

    def put_file(self, request):
        resource = self.get_object()
        if resource.resource_type != RESOURCE_FILE and \
                resource.resource_type != RESOURCE_IMAGE:
            raise ValidationError("File uploading is available only for file and image resources")

        resource_field = resource.field
        if not 'file_data' in request.data:
            raise ValidationError("Field 'file_data' should be set")
        serializer = ResourceFileDataSerializer(
            data={
                'file_data': request.data['file_data'],
                'name': "file",
            }
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(field=resource_field)
            return Response("Success")

