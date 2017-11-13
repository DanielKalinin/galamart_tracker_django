from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, ParseError

class ExtendedModelViewSet(ModelViewSet):

    def get_object_from_query(self, request, queryset, primary=False, field='id'):

        if not field in request.query_params:
            raise ParseError("Field '{}' should be in query params".format(field))

        try:
            obj = queryset.get(pk=int(request.query_params[field]))
        except:
            raise NotFound("Object with this '{}' does not exist".format(field))

        if primary:
            self.check_object_permissions(request, obj)
        return obj

    def get_object(self):
        return self.get_object_from_query(
            self.request,
            self.queryset,
            primary=True,
            field='id',
        )

