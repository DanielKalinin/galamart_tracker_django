import os
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
User = get_user_model()

from .work import Work


def messages_directory_path(message, filetag):
    return 'messages/{0}/{1}/{2}'.format(message.work.id,
                                         message.id,
                                         file_extension)


class Message(models.Model):
    text = models.TextField(max_length=200)
    files = ArrayField(models.FileField(upload_to=messages_directory_path),
                       default=[], blank=True)
    work = models.ForeignKey(Work, related_name='messages', null=True)
    author = models.ForeignKey(User, null=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Project_id={0} Work_id={1} Message_id={2}'. \
            format(self.work.project.id, self.work.id, self.id)

