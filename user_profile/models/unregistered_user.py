from django.db import models
from django.db.models import Q
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
User = get_user_model()

from hel.validators import PhoneValidator
from hel.hashes import sha512
from hel.fields import *
from datetime import datetime


class UnregisteredUser(models.Model):
    email = models.EmailField(unique=True)
    phone = PhoneField()
    password = PasswordField()
    token = models.CharField(max_length=128, unique=True)

    @classmethod
    def create(cls, email, phone, password):
        return cls(
            email=email,
            phone=phone,
            password=sha512(email + password),
            token=sha512(email + str(datetime.now()))
        )

    def clean_matches(self):
        try:
            matches = UnregisteredUser.objects.get(
                Q(email=self.email) | Q(phone=self.phone)
            )
        except UnregisteredUser.DoesNotExist:
            pass
        else:
            matches.delete()

