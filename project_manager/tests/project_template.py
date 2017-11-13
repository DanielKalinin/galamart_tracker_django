from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from hel.user_roles import *

from project_manager.tag_manager import get_by_tag
from project_manager.resource_types import *
from project_manager.models import *
from project_manager.requirements import *


class ProjectTemplateTestCase(TestCase):
    def make_simple_project_template(self, label):
        template = ProjectTemplate.objects.create(
            is_template=True,
            label=label,
            children=['stage1']
        )
        stage = Container.objects.create(
            project=template,
            tag='stage1',
            label="Stage 1",
            children=['desk1']
        )
        desk = Container.objects.create(
            project=template,
            tag='desk1',
            label="Desk 1",
            children=['work1', 'work2']
        )
        work1 = Work.objects.create(
            project=template,
            tag='work1',
            label="Work 1",
            executor_role=ROLE_FRANCHISE,
            requirements=[],
            resources=['res1']
        )
        work2 = Work.objects.create(
            project=template,
            tag='work2',
            label="Work 2",
            executor_role=ROLE_FRANCHISE,
            requirements=['req1'],
            resources=['res2']
        )
        req1 = Requirement.objects.create(
            project=template,
            tag='req1',
            requirement_type=REQUIREMENT_WORK_FINISHED,
            observables=['work1']
        )
        res1 = Resource.objects.create(
            project=template,
            tag='res1',
            label='Resource 1',
            data_type=RESOURCE_TEXT
        )
        res2 = Resource.objects.create(
            project=template,
            tag='res2',
            label='Resource 2',
            data_type=RESOURCE_TEXT
        )
        return template


    def apply_test_to_simple_project(self, project):
        self.assertEqual(project.children, ['stage1'])

        stage = get_by_tag(project, 'stage1')
        self.assertEqual(stage.tag, 'stage1')
        self.assertEqual(stage.label, "Stage 1")
        self.assertEqual(stage.children, ['desk1'])

        desk = get_by_tag(project, 'desk1')
        self.assertEqual(desk.tag, 'desk1')
        self.assertEqual(desk.label, "Desk 1")
        self.assertEqual(desk.children, ['work1', 'work2'])

        work1 = get_by_tag(project, 'work1')
        self.assertEqual(work1.tag, 'work1')
        self.assertEqual(work1.label, "Work 1")
        self.assertEqual(work1.executor_role, ROLE_FRANCHISE)
        self.assertEqual(work1.resources, ['res1'])

        res1 = get_by_tag(project, 'res1')
        self.assertEqual(res1.tag, 'res1')
        self.assertEqual(res1.label, "Resource 1")
        self.assertEqual(res1.data_type, RESOURCE_TEXT)

        work2 = get_by_tag(project, 'work2')
        self.assertEqual(work2.tag, 'work2')
        self.assertEqual(work2.label, "Work 2")
        self.assertEqual(work2.executor_role, ROLE_FRANCHISE)
        self.assertEqual(work2.resources, ['res2'])
        self.assertEqual(work2.requirements, ['req1'])

        res2 = get_by_tag(project, 'res2')
        self.assertEqual(res2.tag, 'res2')
        self.assertEqual(res2.label, "Resource 2")
        self.assertEqual(res2.data_type, RESOURCE_TEXT)

        req1 = get_by_tag(project, 'req1')
        self.assertEqual(req1.tag, 'req1')
        self.assertEqual(req1.requirement_type, REQUIREMENT_WORK_FINISHED)
        self.assertEqual(req1.observables, ['work1'])


    def test_simple_project_template(self):
        project = self.make_simple_project_template("Test")
        self.apply_test_to_simple_project(project)
        self.assertEqual(project.is_template, True)


    def test_project_creation(self):
        user = User.objects.create(
            phone='78005553535',
            email='aa_volkov060999@mail.ru',
            password='sescurfu282',
            role=ROLE_ADMIN
        )
        template = self.make_simple_project_template("Project creation template")
        project = template.buildProject(user)
        self.apply_test_to_simple_project(project)


        self.assertEqual(set(project.participants.all()), set([user]))
        self.assertEqual(project.is_template, False)


    def test_json_project_template_creation(self):
        project = ProjectTemplate.objects.create(label="Kek", is_template=True)
        self.assertEqual(project.label, "Kek")
        json = ('{'
                '   "project": {'
                '       "id": ' + str(project.id) + ','
                '       "label": "Kapodastr",'
                '       "children": ["stage1"]'
                '   },'
                '   "stages": {'
                '       "stage1": {'
                '           "tag": "stage1",'
                '           "label": "Stage 1",'
                '           "children": ["desk1"]'
                '       }'
                '   },'
                '   "desks": {'
                '       "desk1": {'
                '           "tag": "desk1",'
                '           "label": "Desk 1",'
                '           "children": ["work1", "work2"]'
                '       }'
                '   },'
                '   "works": {'
                '       "work1": {'
                '           "tag": "work1",'
                '           "label": "Work 1",'
                '           "executor_role": "' + ROLE_FRANCHISE +'",'
                '           "requirements": [],'
                '           "resources": ["res1"]'
                '       },'
                '       "work2": {'
                '           "tag": "work2",'
                '           "label": "Work 2",'
                '           "executor_role": "' + ROLE_FRANCHISE +'",'
                '           "requirements": ["req1"],'
                '           "resources": ["res2"]'
                '       }'
                '   },'
                '   "requirements": {'
                '       "req1": {'
                '           "tag": "req1",'
                '           "requirement_type": "' + REQUIREMENT_WORK_FINISHED + '",'
                '           "observables": ["work1"]'
                '       }'

                '   },'
                '   "resources": {'
                '       "res1": {'
                '           "tag": "res1",'
                '           "label": "Resource 1",'
                '           "data_type": "' + RESOURCE_TEXT + '"'
                '       },'
                '       "res2": {'
                '           "tag": "res2",'
                '           "label": "Resource 2",'
                '           "data_type": "' + RESOURCE_TEXT + '"'
                '       }'
                '   }'
                '}'
        )
        project = ProjectTemplate.updateFromJSON(json)
        self.apply_test_to_simple_project(project)
        self.assertEqual(project.is_template, True)

