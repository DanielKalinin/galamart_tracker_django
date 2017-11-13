import json
import importlib
from datetime import timedelta
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.exceptions import ValidationError

from project_manager.fields import LabelField, StatusField, TagField
from project_manager.statuses import *

from .project import Project
from .resource import Resource
from .requirement import Requirement
from .work import Work
from .container import Container


class ProjectTemplate(Project):

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_template = True

    @staticmethod
    def copy(instance, project, status=None):
        instance.project = project
        if 'status' in instance.__dict__:
            instance.status = status
        instance.pk = None
        instance.save()

    @staticmethod
    def createFromExistingProject(project):
        template = ProjectTemplate.objects.create()
        works = Work.objects.filter(project=project)
        for work in works:
            self.copy(work, template)
        resources = Resource.objects.filter(project=project)
        for resource in resources:
            self.copy(resource, template)
        containers = Container.objects.filter(project=project)
        for container in containers:
            self.copy(container, template)
        requirements = Requirement.object.filter(project=project)
        for requirement in requirements:
            self.copy(container, template)

    @staticmethod
    def createFromPythonDump(path):
        dump = importlib.import_module(path)
        template = ProjectTemplate.objects.create()
        for work in dump.works:
            work.project = template
            work.save()
        for resource in dump.resources:
            resource.project = template
            resource.save()
        for container in dump.containers:
            container.project = template
            container.save()

    @staticmethod
    def createFromPythonConfig(path):
        dump = importlib.import_module(path)
        template = ProjectTemplate.objects.create()
        counter = 0
        works = {}
        for work in dump.works:
            work.project = template
            work.tag = 'work_{0}'.format(counter)
            counter += 1
            if work.label in works:
                raise Exception("Some shit")
            works[work.label] = work
        for resource in dump.resources: #TODO
            resource.project = template

        for container in dump.containers:
            container.project = template
            container.save()

    @staticmethod
    def validateData(data):
        pass

    @staticmethod
    def updateFromJSON(data):
        try:
            ProjectTemplate.validateData(data)
        except Exception as e:
            raise ValidationError(detail=str(e))

        try:
            project = ProjectTemplate.objects.get(id=data['project']['id'])
        except ProjectTemplate.DoesNotExist:
            return ValidationError(detail="Project id is incorrect")

        objects = []

        if 'requirements' in data:
            for requirement_tag, requirement_data in data['requirements'].items():
                objects.append(Requirement(**requirement_data))

        if 'resources' in data:
            for resource_tag, resource_data in data['resources'].items():
                objects.append(Resource(**resource_data))

        if 'works' in data:
            for work_tag, work_data in data['works'].items():
                if 'duration' in work_data and work_data['duration'] != None:
                    work_data['duration'] = timedelta(hours=work_data['duration'])
                objects.append(Work(**work_data))

        if 'desks' in data:
            for desk_tag, desk_data in data['desks'].items():
                objects.append(Container(**desk_data))

        if 'stages' in data:
            for stage_tag, stage_data in data['stages'].items():
                objects.append(Container(**stage_data))

        project_data = data['project']
        project, created = ProjectTemplate.objects.update_or_create(
            id=project_data['id'],
            defaults=project_data
        )

        Requirement.objects.filter(project=project).delete()
        Resource.objects.filter(project=project).delete()
        Work.objects.filter(project=project).delete()
        Container.objects.filter(project=project).delete()

        for obj in objects:
            obj.project = project
            obj.save()
        return project


    def buildProject(self, creator):
        project = Project.objects.create()
        project.participants.add(creator)
        project.children = self.children

        works = Work.objects.filter(project=self)
        for work in works:
            self.copy(work, project, STATUS_UNAVAILABLE)
        resources = Resource.objects.filter(project=self)
        for resource in resources:
            self.copy(resource, project)
        requirements = Requirement.objects.filter(project=self)
        for requirement in requirements:
            self.copy(requirement, project)
        containers = Container.objects.filter(project=self)
        for container in containers:
            self.copy(container, project)
        return project

