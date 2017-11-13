from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import UnregisteredUser


class UserConfirmSerializer(serializers.Serializer):
    token = serializers.RegexField('^[a-f0-9]{128}$')


class FullUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'patronymic', 'avatar', 'role', 'email', 'phone')
        read_only_fields = ('id', 'role', 'email', 'phone')


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'patronymic', 'avatar', 'role')
        read_only_fields = ('id', 'role')


class UserTmpSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password_repeat = serializers.CharField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with the same email already exists")
        return email

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise ValidationError("Passwords should be same")
        del data['password_repeat']
        return data

    def create(self, validated_data):
        return UnregisteredUser.create(**validated_data)

    class Meta:
        model = UnregisteredUser
        fields = ('email', 'phone', 'password', 'password_repeat')

