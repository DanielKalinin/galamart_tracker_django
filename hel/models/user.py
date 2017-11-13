from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

from hel.fields import *
from hel.hashes import sha512
from hel.validators import PasswordValidator
from hel.user_roles import *


class UserManager(BaseUserManager):

    def create_user(self, email, password, **required_args):
        if not email or not password:
            raise ValueError("Users must have an email address and password")

        user = self.model(email=self.normalize_email(email), **required_args)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **required_args):
        user = self.create_user(email, password, **required_args)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


def avatar_directory_path(instance, filetag):
    return 'avatar/{0}__{1}'.format(instance.pk, filetag)


class User(AbstractBaseUser):
    name = NameField(blank=True, null=True)
    surname = NameField(blank=True, null=True)
    patronymic = NameField(blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_directory_path,
                               default='avatars/default.png', blank=True)
    role = RoleField(blank=True, null=True)

    email = models.EmailField(unique=True)
    phone = PhoneField(unique=True)
    password = PasswordField()

    # Methods and fields for enabling authentication on this model

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = True

    @classmethod
    def create_from_unregistered(cls, unregistered_user):
        user = cls(
            email = unregistered_user.email,
            phone = unregistered_user.phone,
            password = unregistered_user.password,
            role = ROLE_FRANCHISE
        )
        return user

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def set_password(self, raw_password):
        PasswordValidator(raw_password)
        if self.email:
            self.password = sha512(self.email + raw_password)

    def check_password(self, raw_password):
        return self.password == sha512(self.email + raw_password)

    def get_full_name(self):
        return '{0} {1}'.format(self.name, self.surname)

    def get_short_name(self):
        return self.name


