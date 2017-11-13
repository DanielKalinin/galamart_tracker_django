import traceback

from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ImproperlyConfigured

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.compat import six
from rest_framework.utils import model_meta

from generic_relations.relations import GenericRelatedField

from project_manager.models import (
    Project,
    ProjectTemplate,
    Work,
    Message,
    Requirement,
    Resource,
    ResourceTextField,
    ResourceSelectField,
    ResourceCheckboxField,
    ResourceFileField,
    ResourceFileData,
    ResourceUserSelectField,
    Container,
)
from hel.serializers import UserSerializer
from project_manager.tag_manager import get_by_tag


class ChoicesField(serializers.Field):

    def get_attribute(self, obj):
        if 'attr' not in self.__dict__:
            self.attr = self.source_attrs[-1]
            self.source_attrs = self.source_attrs[:-1]
        return super().get_attribute(obj)

    def to_representation(self, obj):
        raw = getattr(obj, self.attr)
        readable = (getattr(obj, 'get_{0}_display'.format(self.attr)))()
        return (raw, readable)


class ResourceTextFieldSerializer(serializers.ModelSerializer):

    def validate_text(self, value):
        if not isinstance(value, str):
            raise ValidationError("Text field must be a string")
        return value

    class Meta:
        model = ResourceTextField
        fields = ('text',)

class ResourceUserSelectFieldSerializer(serializers.ModelSerializer):

    users = UserSerializer(read_only=True, many=True)
    user_selected = UserSerializer(User.objects.all())

    class Meta:
        model = ResourceUserSelectField
        fields = ('user_role','users','user_selected')


class ResourceFileDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResourceFileData
        fields = ('name', 'file_data')


class ResourceFileFieldSerializer(serializers.ModelSerializer):
    files = ResourceFileDataSerializer(ResourceFileData.objects.all(), many=True)

    class Meta:
        model = ResourceFileField
        fields = ('files',)


class ResourceSelectSerializer(serializers.ModelSerializer):

    def validate_options(self, value):
        if not isinstance(value, dict):
            raise ValidationError("Options field must be a dict")
        for k, v in value.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValidationError("Options field must contain only strings")
        return value

    def validate_selected(self, value):
        if not isinstance(value, str):
            raise ValidationError("Selected field must be a string")
        return value

    class Meta:
        model = ResourceSelectField
        fields = ('options', 'selected')
        read_only_fields = ('options',)


class ResourceCheckboxSerializer(serializers.ModelSerializer):

    def validate_selected(self, value):
        if not isinstance(value, list) or not isinstance(value, tuple):
            raise ValidationError("Selected field must be an array")
        return value

    class Meta:
        model = ResourceCheckboxField
        fields = ('options', 'selected')
        read_only_fields = ('options',)


class NewGenericRelatedField(GenericRelatedField):

    def run_validation(self, data):
        try:
            serializer = self.get_deserializer_for_data()
        except ImproperlyConfigured as e:
            raise ValidationError(e)
        return serializer.run_validation(data)

    def to_internal_value(self, data):
        try:
            serializer = self.get_deserializer_for_data()
        except ImproperlyConfigured as e:
            raise ValidationError(e)
        return serializer.to_internal_value(data)

    def get_deserializer_for_data(self):
        serializers = []
        for model, serializer in self.serializers.items():
            if model == self.parent.instance.field.__class__:
                # Collects all serializers that can handle the input data.
                serializers.append(serializer)

        # If no serializer found, raise error.
        l = len(serializers)
        if l < 1:
            raise ImproperlyConfigured(
                'Could not determine a valid serializer for value.')
        elif l > 1:
            raise ImproperlyConfigured(
                'There were multiple serializers found for value.')
        return serializers[0]


class ResourceSerializer(serializers.ModelSerializer):
    resource_type = ChoicesField(read_only=True)
    field = NewGenericRelatedField({
        ResourceTextField: ResourceTextFieldSerializer(),
        ResourceFileField: ResourceFileFieldSerializer(),
        ResourceUserSelectField: ResourceUserSelectFieldSerializer(),
        ResourceSelectField: ResourceSelectSerializer(),
        ResourceCheckboxField: ResourceCheckboxSerializer(),
    })

    def update(self, instance, validated_data):
        field_data = validated_data.pop('field')
        instance = super().update(instance, validated_data)

        field = getattr(instance, 'field')
        for attr in field_data:
            setattr(field, attr, field_data[attr])
        try:
            field.is_valid(raise_exception=True)
        except ValidationError as e:
            raise ValidationError({'field': e.detail})

        field.save()
        instance.save()

        return instance

    class Meta:
        model = Resource
        fields = ('tag', 'label', 'resource_type', 'field')
        read_only_fields = ('tag', 'label', 'resource_type')

    #def validate(self, data):  # TODO: Rework
    #    if not self.instance:
    #        raise Exception("ResourceSerializer requires instance")
    #    text_data = data.get('text_data', None)
    #    file_data = data.get('file_data', None)
    #    if not self.instance.is_valid(text_data, file_data):
    #        raise ValidationError("data sent to resource is incorrect")
    #    return data


class ContainerSerializer(serializers.ModelSerializer):
    children = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Container
        fields = ('label', 'children', 'is_leaf')


class ProjectSerializer(serializers.ModelSerializer):

    def save(self, *args, request=None, template_id=None, **kwargs):
        self.request = request
        self.template_id = template_id
        self.validated_data['is_template'] = False
        return super().save(*args, **kwargs)

    def create(self, validated_data):
        if not self.request:
            raise Exception("Project creation failed: request is required")
        if not self.template_id:
            raise Exception("Project creation failed: template_id is required")

        try:
            self.template = ProjectTemplate.objects.get(is_template=True, pk=self.template_id)
        except ProjectTemplate.DoesNotExist:
            raise ValidationError("Template with this id does not exist")

        try:
            project = self.template.buildProject(self.request.user)
        except AttributeError:
            return ValidationError("Authorization is required")

        for field, value in validated_data.items():
            setattr(project, field, value)
        return project


    class Meta:
        model = Project
        fields = ('id', 'label', 'startdate', 'enddate', 'participants', 'status', 'children')
        read_only_fields = ('id', 'startdate', 'enddate', 'participants', 'status', 'children')


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('text', 'files', 'author', 'datetime')
        read_only_fields = ('author', 'datetime')


class WorkSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    resources = serializers.SerializerMethodField()
    status = ChoicesField()
    executor_role = ChoicesField()
    verifier_role = ChoicesField()

    def get_resources(self, work):
        resources = [get_by_tag(work.project, tag) for tag in work.resources]
        serializer = ResourceSerializer(resources, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Work
        fields = ('id', 'tag', 'label', 'status', 'startdate', 'resources',
                  'enddate', 'duration', 'executor', 'verifier', 'executor_role',
                  'verifier_role', 'messages', 'history')


