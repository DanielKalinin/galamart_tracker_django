from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth import get_user_model
User = get_user_model()

from project_manager.fields import StatusField, LabelField, TagField
from project_manager.statuses import *
from project_manager.decorators import require_status
from project_manager.tag_manager import get_by_tag

class Project(models.Model):
    label = LabelField()
    startdate = models.DateTimeField(null=True, blank=True)
    enddate = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True)
    status = StatusField()
    children = ArrayField(TagField(), default=[], blank=True)
    is_template = models.BooleanField(default=False)

    @property
    def children_representation(self):
        return [get_by_tag(self, tag) for tag in self.children]

    def find_user(self, role):
        #TODO: write user statistics and choose least working user, if len > 1
        user = self.participants.filter(role=role).first()
        if not user:
            #TODO: write user statistics and choose least working user
            user = User.objects.filter(role=role).first()
        return user

    def change_status(self, status):
        self.status = status
        self.save()

    @require_status(STATUS_UNAVAILABLE)
    def open(self):
        self.change_status(STATUS_IN_PROGRESS)
        for tag in self.children:
            object = get_by_tag(self, tag)
            object.open()
        return True

    @require_status(STATUS_IN_PROGRESS)
    def complete(self):
        self.change_status(STATUS_DONE)
        return True

    def __str__(self):
        return '({0}) {1}'.format(self.id, self.label)

