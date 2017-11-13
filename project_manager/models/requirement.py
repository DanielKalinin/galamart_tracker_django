from django.db import models
from django.contrib.postgres.fields import ArrayField

from project_manager import requirements
from project_manager.fields import TagField
from project_manager.requirements import *
from .project import Project


class Requirement(models.Model):
    tag = TagField()
    project = models.ForeignKey(Project, null=True, blank=True,
                                on_delete=models.CASCADE)
    requirement_type = models.CharField(max_length=255, choices=REQUIREMENT_TYPES_LIST)
    observables = ArrayField(models.CharField(max_length=255), default=[])

    def check_requirement(self):
        func = getattr(requirements, self.requirement_type)
        if not func(self.project, *self.observables):
            return False
        return True

    def __str__(self):
        return '({0}) {1}'.format(self.project.id, self.tag)

