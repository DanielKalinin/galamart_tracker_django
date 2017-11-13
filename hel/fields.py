from django.db import models
from .user_roles import ROLE_LIST
from .validators import *

class RoleField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 60
        kwargs['choices'] = ROLE_LIST
        super().__init__(*args, **kwargs)

class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 30
        kwargs['validators'] = [NameValidator]
        super().__init__(*args, **kwargs)

class PhoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        kwargs['validators'] = [PhoneValidator]
        super().__init__(*args, **kwargs)

class PasswordField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 128
        kwargs['validators'] = [HashedPasswordValidator]
        super().__init__(*args, **kwargs)
