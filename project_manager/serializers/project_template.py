from rest_framework import serializers

from project_manager.models import ProjectTemplate, Container, Work, Requirement, Resource
from project_manager.tag_manager import get_by_tag


class ProjectTemplateSerializer(serializers.ModelSerializer):

    def save(self, *args, **kwargs):
        self.validated_data['is_template'] = True
        return super().save(*args, **kwargs)

    class Meta:
        model = ProjectTemplate
        fields = ('id', 'label', 'children')
        read_only_fields = ('children',)


class ContainerTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Container
        fields = ('tag', 'label', 'children')
        read_only_fields = ('children',)


class WorkTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Work
        fields = ('tag', 'label', 'requirements', 'resources', 'enddate', 'duration', 'executor_role', 'verifier_role', 'executor_text', 'verifier_text', 'is_goal')
        read_only_fields = ('requirements', 'resources')


class RequirementTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requirement
        fields = ('tag', 'requirement_type', 'observables')


class ResourceTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ('tag', 'label', 'data_type', 'text_data')



# Serializers for JSON representation of the project


class ProjectJSONSerializer(serializers.BaseSerializer):

    def to_representation(self, project):
        data = {
            'project': ProjectTemplateSerializer(project).data,
            'stages': [],
            'desks': [],
            'works': [],
            'requirements': [],
            'resources': [],
        }
        for stage_tag in project.children:
            stage = get_by_tag(project, stage_tag)
            data['stages'].append(ContainerTemplateSerializer(stage).data)
            for desk_tag in stage.children:
                desk = get_by_tag(project, desk_tag)
                data['desks'].append(ContainerTemplateSerializer(desk).data)
                for work_tag in desk.children:
                    work = get_by_tag(project, work_tag)
                    data['works'].append(WorkTemplateSerializer(work).data)
                    for requirement_tag in work.requirements:
                        requirement = get_by_tag(project, requirement_tag)
                        data['requirements'].append(RequirementTemplateSerializer(requirement).data)
                    for resource_tag in work.resources:
                        resource = get_by_tag(project, resource_tag)
                        data['resources'].append(ResourceTemplateSerializer(resource).data)
        return data


