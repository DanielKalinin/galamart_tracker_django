from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.postgres.fields import JSONField, ArrayField

from rest_framework.exceptions import ValidationError

from hel.user_roles import *
from hel.fields import RoleField
from .resource import Resource


def resource_directory_path(instance, filetag):
    return 'resources/{0}__{1}/{2}'.format(
        instance.field.resource.tag,
        instance.field.resource.project.id,
        filetag
    )


class ResourceFieldMixin(object):
    @property
    def resource(self):
        return self._resource.get()


class ResourceTextField(ResourceFieldMixin, models.Model):
    _resource = GenericRelation(Resource)
    text = models.CharField(max_length=1024)

    def is_valid(self, raise_exception=False):
        return True


class ResourceFileField(ResourceFieldMixin, models.Model):
    _resource = GenericRelation(Resource)

    def is_valid(self, raise_exception=False):
        return True


class ResourceFileData(models.Model):
    field = models.ForeignKey(ResourceFileField, related_name='files')
    name = models.CharField(max_length=256)
    file_data = models.FileField(upload_to=resource_directory_path, max_length=255)


class ResourceUserSelectField(models.Model):
    resource = GenericRelation(Resource)
    user_role = RoleField()
    user_selected = models.ForeignKey(User, null=True, blank=True)

    @property
    def users(self):
        return User.objects.filter(role = self.user_role)


class ResourceSelectField(ResourceFieldMixin, models.Model):
    _resource = GenericRelation(Resource)
    options = JSONField()
    selected = models.CharField(max_length=256, null=True, blank=True)

    def is_valid(self, raise_exception=False):
        try:
            if self.selected not in self.options:
                raise ValidationError("Selected field should be in the options field")
        except ValidationError as e:
            if raise_exception:
                raise e
            return False
        else:
            return True

class ResourceCheckboxField(ResourceFieldMixin, models.Model):
    _resource = GenericRelation(Resource)
    options = JSONField()
    selected = ArrayField(models.CharField(max_length=256), default=[])

    def is_valid(self, raise_exception=False):
        try:
            if self.selected not in self.options:
                raise ValidationError("Selected field should be contained in the options field")
        except ValidationError as e:
            if raise_exception:
                raise e
            return False
        else:
            return True

