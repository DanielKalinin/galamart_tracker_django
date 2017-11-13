from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from hel.viewsets import ExtendedModelViewSet
from hel.decorators import for_authorized, for_appointed
from hel.email import send_mail
from .models import UnregisteredUser
from .permissions import (
    IsNotCreationOrIsNotAuthorized,
)
from .serializers import (
    FullUserSerializer,
    ShortUserSerializer,
    UserTmpSerializer,
    UserConfirmSerializer,
)


class UserViewSet(ExtendedModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsNotCreationOrIsNotAuthorized,)

    def get_serializer_class(self):
        user = self.request.user
        if self.action == 'create':
            return UserTmpSerializer
        elif self.action == 'confirm':
            return UserConfirmSerializer
        elif self.action == 'personal':
            return FullUserSerializer
        elif self.action == 'retrieve':
            if user and user.is_superuser or\
                user == self.get_object():
                return FullUserSerializer
            return ShortUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            unregistered_user = serializer.save()
            unregistered_user.clean_matches()
            unregistered_user.save()
            send_mail(
                "Регистрация",
                unregistered_user.token,
                "example@site.com",
                unregistered_user.email
            )
        return Response("Token has been sent")

    def confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.data['token']
            try:
                unregistered_user = UnregisteredUser.objects.get(token=token)
            except UnregisteredUser.DoesNotExist:
                return ValidationError({"token": "Invalid token"})
            user = User.create_from_unregistered(unregistered_user)
            unregistered_user.delete()
            user.save()
            return Response("Success")

    def personal(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

