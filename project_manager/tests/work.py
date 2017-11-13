from django.test import TestCase
from datetime import timedelta
from hel.models import User
from hel.user_roles import *


from project_manager.resource_types import *
from project_manager.models import *
from project_manager.statuses import *
from project_manager.requirements import *

from project_manager.models import *
from project_manager.statuses import *


class WorkTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create()
        self.req1 = Requirement.objects.create(tag='req1', project=self.project,
                                               requirement_type=REQUIREMENT_WORK_FINISHED,
                                               observables=['Work 1'])
        self.req2 = Requirement.objects.create(tag='req2', project=self.project,
                                               requirement_type=REQUIREMENT_WORK_FINISHED,
                                               observables=['Work 2'])
        self.work1 = Work.objects.create(tag="Work 1", project=self.project,
                                         executor_role=ROLE_FRANCHISE,
                                         verifier_role=ROLE_COORDINATOR)
        self.work2 = Work.objects.create(tag="Work 2", project=self.project,
                                         executor_role=ROLE_FRANCHISE,
                                         verifier_role=ROLE_PROJECT_MANAGER,
                                         requirements=['req1'])
        self.work3 = Work.objects.create(tag="Work 3", project=self.project,
                                         executor_role=ROLE_PROJECT_MANAGER,
                                         verifier_role=ROLE_COORDINATOR,
                                         requirements=['req2'])
        self.user1 = User.objects.create(name="Вася", surname="kek",
                                         patronymic="cheburek",
                                         email="hello@mail.ru",
                                         phone="11111111111",
                                         password="jjjjjjjjjjjjjjjjjjjjjjjjjj",
                                         role=ROLE_FRANCHISE)
        self.user2 = User.objects.create(name="Петя", surname="kek",
                                         patronymic="cheburek",
                                         email="ho@mail.ru",
                                         phone="11111211111",
                                         password="iiiiiiiiiiiiiiiiiiiiiiiiii",
                                         role=ROLE_COORDINATOR)
        self.user3 = User.objects.create(name="Коля", surname="kek",
                                         patronymic="cheburek",
                                         email="hoi@mail.ru",
                                         phone="11311211111",
                                         password="iiiiiiiiiiiiiiiiiiiiiiiiii",
                                         role=ROLE_PROJECT_MANAGER)
        self.project.participants.add(self.user1, self.user2, self.user3)

    def test_work_dependencies_old_wihtout_descendants_checking(self):
        self.work1.open()
        self.work2.open()
        self.assertEqual(self.work2.status, STATUS_UNAVAILABLE)
        self.work1.start()
        self.work1.complete()
        self.work1.verify()
        self.assertEqual(self.work1.status, STATUS_DONE)
        self.work1.save()
        self.work2.open()
        self.assertEqual(self.work2.status, STATUS_AWAITING_WORK)
        self.work3.open()
        self.assertEqual(self.work3.status, STATUS_UNAVAILABLE)
        self.work2.start()
        self.work2.complete()
        self.work2.verify()
        self.work2.save()
        self.work3.open()
        self.assertEqual(self.work3.status, STATUS_AWAITING_WORK)

    def test_work_dependencies(self):
        self.work1.open()
        self.work2.open()
        self.assertEqual(self.work2.status, STATUS_UNAVAILABLE)
        self.work1.start()
        self.work1.complete()
        self.work1.verify()
        self.assertEqual(self.work1.status, STATUS_DONE)
        self.work1.save()
        self.work2 = Work.objects.get(pk=self.work2.pk)
        self.assertEqual(self.work2.status, STATUS_AWAITING_WORK)
        self.work3.open()
        self.assertEqual(self.work3.status, STATUS_UNAVAILABLE)
        self.work2.start()
        self.work2.complete()
        self.work2.verify()
        self.work2.save()
        self.work3 = Work.objects.get(pk=self.work3.pk)
        self.assertEqual(self.work3.status, STATUS_AWAITING_WORK)


class CountDateStart(TestCase):
    def test_count_prediction_date(self):
        project = Project.objects.create()
        parents_list = [[], [3], [1], [1, 3], [4], [2], [6, 3]]
        self.__dict__ = {**self.__dict__, **{'work{}'.format(i): Work.objects.create(tag='work{}'.format(i), project=project, executor_role=ROLE_COORDINATOR, duration=timedelta(seconds=10),status=STATUS_UNAVAILABLE, requirements=['req{}{}'.format(p, i) for p in parents_list[i - 1]]) for i in range(1, len(parents_list) + 1)}}
        self.__dict__ = {**self.__dict__, **{'req{}{}'.format(p, c): Requirement.objects.create(tag='req{}{}'.format(p, c), requirement_type=REQUIREMENT_WORK_FINISHED, observables=['work{}'.format(p)], project=project) for c in range(1, len(parents_list) + 1) for p in parents_list[c - 1]}}
        self.work1.count_prediction_date()

