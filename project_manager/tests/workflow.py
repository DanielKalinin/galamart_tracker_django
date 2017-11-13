from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from hel.user_roles import *

from project_manager.statuses import *
from project_manager.models import *



class SimplestTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(label="Project",
                                         children=['stage1'])

        self.stage1 = Container.objects.create(project=self.project,
                                 label="Stage 1",
                                 tag='stage1',
                                 children=['desk1_1', 'desk1_2'])

        self.desk1_1 = Container.objects.create(project=self.project,
                                 label="Desk 1 1",
                                 tag='desk1_1',
                                 children=['work1_1_1', 'work1_1_2'])
        self.desk1_2 = Container.objects.create(project=self.project,
                                 label="Desk 1 2",
                                 tag='desk1_2',
                                 children=['work1_2_1'])

        self.work1_1_1 = Work.objects.create(project=self.project,
                            label="Work 1 1 1",
                            tag='work1_1_1',
                            executor_role=ROLE_FRANCHISE,
                            verifier_role=ROLE_COORDINATOR)
        self.work1_1_2 = Work.objects.create(project=self.project,
                            label="Work 1 1 2",
                            tag='work1_1_2',
                            executor_role=ROLE_FRANCHISE,
                            verifier_role=ROLE_COORDINATOR)
        self.work1_2_1 = Work.objects.create(project=self.project,
                            label="Work 1 2 1",
                            tag='work1_2_1',
                            executor_role=ROLE_COORDINATOR,
                            verifier_role=ROLE_FRANCHISE)

        self.req1 = Requirement.objects.create(

        self.franch = User.objects.create(name="Вася", surname="kek", patronymic="cheburek",
                            email="hello@mail.ru", phone="11111111111",
                            password="abcdefgh1234",
                            role=ROLE_FRANCHISE)
        self.coord = User.objects.create(name="Петя", surname="kek", patronymic="cheburek",
                            email="ho@mail.ru", phone="11111211111",
                            password="abcdefgh1234",
                            role=ROLE_COORDINATOR)

    def test_simplest_workflow(self):
        self.assertEqual(self.stage1.is_available(), False, "Stage 1 is available")
        self.assertEqual(self.desk1_1.is_available(), False, "Desk 1 1 is available")
        self.assertEqual(self.desk1_2.is_available(), False, "Desk 1 2 is available")
        self.assertEqual(self.work1_1_1.is_available(), False, "Work 1 1 1 is avaliable")
        self.assertEqual(self.work1_1_2.is_available(), False, "Work 1 1 2 is available")
        self.assertEqual(self.work1_2_1.is_available(), False, "Work 1 2 1 is available")

        self.assertEqual(self.stage1.has_access(self.franch), False, "Stage 1 is accessible")
        self.assertEqual(self.desk1_1.has_access(self.franch), False, "Desk 1 1 is accessible")
        self.assertEqual(self.desk1_2.has_access(self.franch), False, "Desk 1 2 is accessible")
        self.assertEqual(self.work1_1_1.has_access(self.franch), False, "Work 1 1 1 is accessible")
        self.assertEqual(self.work1_1_2.has_access(self.franch), False, "Work 1 1 2 is accessible")
        self.assertEqual(self.work1_2_1.has_access(self.franch), False, "Work 1 2 1 is accessible")

        self.assertEqual(self.stage1.has_access(self.coord), False, "Stage 1 is accessible")
        self.assertEqual(self.desk1_1.has_access(self.coord), False, "Desk 1 1 is accessible")
        self.assertEqual(self.desk1_2.has_access(self.coord), False, "Desk 2 2 is accessible")
        self.assertEqual(self.work1_1_1.has_access(self.coord), False, "Work 1 1 1 is accessible")
        self.assertEqual(self.work1_1_2.has_access(self.coord), False, "Work 1 1 2 is accessible")
        self.assertEqual(self.work1_2_1.has_access(self.coord), False, "Work 1 2 1 is accessible")

        self.project.participants.add(self.franch)
        self.project.participants.add(self.coord)

        self.work1_1_1.open()
        self.assertEqual(self.work1_1_1.executor, self.franch, "executor not selected")
        self.assertEqual(self.work1_1_1.verifier, self.coord, "verifier not selected")
        self.assertEqual(self.work1_1_1.status, STATUS_AWAITING_WORK, "work 1 1 1 not opened")
        self.work1_1_1.start()
        self.assertEqual(self.work1_1_1.status, STATUS_IN_PROGRESS, "work 1 1 1 not started")
        self.work1_1_1.complete()
        self.assertEqual(self.work1_1_1.status, STATUS_AWAITING_VERIFICATION, "work 1 1 1 not completed")
        self.work1_1_1.verify()
        self.assertEqual(self.work1_1_1.status, STATUS_DONE, "work 1 1 1 not done")


