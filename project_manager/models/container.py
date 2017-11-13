from django.db import models
from django.contrib.postgres.fields import ArrayField

from project_manager.fields import TagField, LabelField
from project_manager.tag_manager import get_by_tag
from .project import Project

class Container(models.Model):
    tag = TagField()
    label = LabelField()
    project = models.ForeignKey(Project)
    children = ArrayField(TagField(), default=[], blank=True)
    is_leaf = models.BooleanField(default=False)

    @property
    def children_representation(self):
        return [get_by_tag(self.project, tag) for tag in self.children]

    def is_available(self):
        for children_tag in self.children:
            if get_by_tag(self.project, children_tag).is_available():
                return True
        return False

    def has_access(self, user):
        for children_tag in self.children:
            if get_by_tag(self.project, children_tag).has_access(user):
                return True
        return False

    def open(self):
        for tag in self.children:
            object = get_by_tag(self.project, tag)
            object.open()
        return True

    def __str__(self):
        return '({}) {}'.format(self.project.id, self.tag)


