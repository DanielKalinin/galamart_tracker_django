from datetime import timedelta
from functools import wraps
import logging
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, DateRangeField, JSONField
from django.utils.timezone import localtime, now
from hel.models.user import User
from hel.fields import RoleField
from project_manager.requirements import *
from project_manager.statuses import *
from project_manager.fields import TagField, StatusField, LabelField
from project_manager.tag_manager import get_by_tag
from project_manager.access_levels import *
from project_manager.decorators import require_status, prohibit_status
from .project import Project
from .requirement import Requirement

logger = logging.getLogger('worklog')

class Work(models.Model):
    tag = TagField()
    label = LabelField()
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    startdate = models.DateTimeField(null=True, blank=True)
    enddate = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    executor = models.ForeignKey(User, related_name="works",
                                 null=True, blank=True)
    verifier = models.ForeignKey(User, related_name="verifications",
                                 null=True, blank=True)
    executor_role = RoleField(null=True, blank=True)
    verifier_role = RoleField(null=True, blank=True)
    executor_text = models.TextField(blank=True, null=True)
    verifier_text = models.TextField(blank=True, null=True)
    status = StatusField()
    requirements = ArrayField(TagField(), default=[], blank=True)
    resources = ArrayField(TagField(), default=[], blank=True)
    history = JSONField(default={}, blank=True)
    is_goal = models.BooleanField(default=False)
    time_to_activate = models.DurationField(null=True, blank=True)

    @property
    def requirements_representation(self):
        return [get_by_tag(self.project, tag) for tag in self.requirements]

    @property
    def resources_representation(self):
        return [get_by_tag(self.project, tag) for tag in self.resources]

    def has_access(self, user):
        return user == self.verifier or user == self.executor

    def is_available(self):
        return self.status != STATUS_UNAVAILABLE

    def change_status(self, status):
        timestamp = str(localtime(now()))
        self.history[timestamp] = status
        self.status = status
        self.save()
        logger.info(str.join(',',[status,str(self.id)]))

    def require_executor(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self.executor = self.project.find_user(self.executor_role)
            if not self.executor:
                raise Exception("Cannot " + method.__name__ + "() Work " \
                                + "instance, executor required")
            return method(self, *args, **kwargs)
        return wrapper

    def require_verifier(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self.verifier = self.project.find_user(self.verifier_role)
            if self.verifier_role and not self.verifier:
                raise Exception("Cannot " + method.__name__ + "() Work " \
                                + "instance, verifier required")
            return method(self, *args, **kwargs)
        return wrapper

    def activate_pridiction_date(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self.count_prediction_date()
            return method(self, *args, **kwargs)
        return wrapper


    def check_visibility_access(self, user):
        privileges = ACCESS_LIST[user.role]
        return ACCESS_SEE_ALL in priveleges or \
            user.role == self.executor or user.role == self.verifier

    def check_review_access(self, user):
        privileges = ACCESS_LIST[user.role]
        return ACCESS_REVIEW_ALL in priveleges or \
            user.role == self.executor or user.role == self.verifier

    def check_modification_access(self, user):
        privileges = ACCESS_LIST[user.role]
        return ACCESS_MODIFY_ALL in priveleges or user.role == self.executor

    @require_status(STATUS_UNAVAILABLE, STATUS_REACTIVATED)
    def open(self):
        if not self.check_requirements():
            return False
        self.executor = self.project.find_user(self.executor_role)
        self.verifier = self.project.find_user(self.verifier_role)
        self.change_status(STATUS_AWAITING_WORK)
        self.save()
        return True

    @require_status(STATUS_AWAITING_WORK)
    @require_executor
    def start(self):
        self.change_status(STATUS_IN_PROGRESS)
        return True

    @require_status(STATUS_IN_PROGRESS)
    def complete(self):
        self.change_status(STATUS_AWAITING_VERIFICATION)
        if not self.verifier_role:
            self.verify()
        return True

    @require_status(STATUS_AWAITING_VERIFICATION)
    @require_verifier
    def verify(self):
        self.change_status(STATUS_DONE)
        if self.is_goal:
            if not len(Work.objects.filter(project=self.project, is_goal=True).exclude(status=STATUS_DONE)):
                self.project.complete()
            return True
        requirements = list(Requirement.objects.filter(
                                                    requirement_type=REQUIREMENT_WORK_FINISHED,
                                                    observables__contains=[self.tag]))
        requirement_tag = [r.tag for r in requirements]
        descendants = self.project.work_set.filter(
            requirements__overlap=requirement_tag
        )
        for work in descendants:
            work.open()
        return True

    @require_status(STATUS_AWAITING_VERIFICATION)
    @require_verifier
    def deny(self):
        self.change_status(STATUS_AWAITING_WORK)
        return True

    def check_requirements(self):
        if not self.requirements:
            return True
        for requirement_tag in self.requirements:
            requirement = get_by_tag(self.project, requirement_tag)
            if not requirement.check_requirement():
                return False
        return True

    def find_executor(self):
        try:
            self.executor = self.project.find_user(self.executor_role)
        except User.DoesNotExist:
            return False
        return True

    def find_verifier(self):
        if self.verifier_role:
            try:
                self.verifier = self.project.find_user(self.verifier_role)
            except User.DoesNotExist:
                return False
        return True

    def is_finished(self):
        return STATUS_DONE == self.status

    @prohibit_status(STATUS_UNAVAILABLE)
    def reactivate(self,open=True):
        self.change_status(STATUS_REACTIVATED)
        self.save()
        if open:
            self.open()
        works = Work.objects.filter(project = self.project).exclude(status=STATUS_UNAVAILABLE)
        children = [work for work in works if work.is_child(self)]
        for child in children:
            child.reactivate(open=False)
        return True

    def post_message(self, user, message):
        if user != self.verifier and user != self.executor:
            raise Exception("User is not allowed to chat")
        self.chat.append({
            'author': user.pk,
            'timestamp': localtime(now()),
            'message': str(message),
        })

    def count_prediction_date(self):
        import itertools
        works = Work.objects.filter(project=self.project).exclude(status=STATUS_DONE)
        edges = [(work1, work2) for work1, work2 in itertools.product(works, works) if work2.is_child(work1)]
        inf = timedelta(days=1000)
        for work in works:
            work.time_to_activate = inf if (work.status == STATUS_UNAVAILABLE) else timedelta()
        for i in works:
            for edge in edges:
                if edge[0].time_to_activate < inf:
                    edge[1].time_to_activate = min(edge[1].time_to_activate, edge[0].time_to_activate + edge[0].duration)
        for work in works:
            work.save()


    def is_child(self, work):
        return len(list(filter(lambda req: req.requirement_type == REQUIREMENT_WORK_FINISHED and req.observables == [work.tag], [get_by_tag(self.project, req_tag) for req_tag in self.requirements]))) != 0



    def __str__(self):
        return '({0}) {1}'.format(self.project.id, self.tag)

