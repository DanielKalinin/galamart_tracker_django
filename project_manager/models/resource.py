from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from hel.user_roles import ROLE_LIST

from project_manager.fields import TagField, ResourceTypeField, LabelField
from project_manager.models import Project


class Resource(models.Model):
    tag = TagField()
    label = LabelField()
    resource_type = ResourceTypeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    field = GenericForeignKey()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

