from django.db import models
from .statuses import STATUS_LIST, STATUS_UNAVAILABLE
from .resource_types import RESOURCE_LIST

class StatusField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = STATUS_LIST
        kwargs['default'] = STATUS_UNAVAILABLE
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

class TagField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super().__init__(*args, **kwargs)

class ResourceTypeField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = RESOURCE_LIST
        super().__init__(*args, **kwargs)

class LabelField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)
