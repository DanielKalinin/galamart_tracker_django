from django.test import TestCase

from hel.user_roles import *

from project_manager.resource_types import *
from project_manager.models import *


class ResourceTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(is_template=True, label="Test Project")
        resources = [
            ('resource_text', RESOURCE_TEXT),
            ('resource_select', RESOURCE_SELECT),
            ('resource_checkbox', RESOURCE_CHECKBOX),
            ('resource_image', RESOURCE_IMAGE),
            ('resource_file', RESOURCE_FILE),
            ('resource_user_select', RESOURCE_USER_SELECT)
        ]
        for resource in resources:
            self.__dict__[resource[0]] = Resource.objects.create(
                tag=resource[0],
                label=resource[0],
                project=self.project,
                data_type=resource[1],
            )

    def test_resource_text(self):
        self.assertEqual(self.resource_text.is_valid(), False,
                         "Empty resource_text is considered as valid")
        self.assertEqual(self.resource_text.data_type, RESOURCE_TEXT,
                         "resource_text type is incorrect")
        self.resource_text.text_data = 'Hello darkness my old friend'
        self.assertEqual(self.resource_text.is_valid(), True,
                         "Valid resource_text is considered as not valid")
        self.assertEqual(self.resource_text.text, "Hello darkness my old friend",
                         "resource_text doesn't save text")
        self.resource_text.file_data = ['file_name']
        self.assertEqual(self.resource_text.is_valid(), False,
                         "Not valid resource_text is considered as valid")

    def test_resource_select(self):
        self.assertEqual(self.resource_select.is_valid(), False,
                         "Empty resource_select is considered as valid")
        self.assertEqual(self.resource_select.data_type, RESOURCE_SELECT,
                         "resource_select type is incorrect")
        self.resource_select.text_data = { "options": ["o1","o2","o3","o4"], "selected": "o2" }
        self.assertEqual(self.resource_select.is_valid(), True,
                         "Valid resource_select is considered as not valid")
        self.assertEqual(self.resource_select.options, ["o1", "o2", "o3", "o4"],
                         "resource_select options don't work properly")
        self.assertEqual(self.resource_select.selected, "o2",
                         "resource_select selected doesn't work properly")
        self.resource_select.file_data = ['file_name']
        self.assertEqual(self.resource_select.is_valid(), False,
                         "Not valid resource_select is considered as valid")

    def test_resource_checkbox(self):
        self.assertEqual(self.resource_checkbox.is_valid(), False,
                         "Empty resource_checkbox is considered as valid")
        self.assertEqual(self.resource_checkbox.data_type, RESOURCE_CHECKBOX,
                         "resource_checkbox type is incorrect")
        self.resource_checkbox.text_data = { "options": ["o1","o2","o3","o4"], "selected": ["o2","o4"] }
        self.assertEqual(self.resource_checkbox.is_valid(), True,
                         "Valid resource_checkbox is considered as not valid")
        self.assertEqual(self.resource_checkbox.options, ["o1", "o2", "o3", "o4"],
                         "resource_checkbox options don't work properly")
        self.assertEqual(self.resource_checkbox.selected, ["o2", "o4"],
                         "resource_checkbox selected don't work properly")
        self.resource_checkbox.file_data = ['file_name']
        self.assertEqual(self.resource_checkbox.is_valid(), False,
                         "Not valid resource_checkbox is considered as valid")

    def test_resource_user_select(self):
        self.assertEqual(self.resource_user_select.is_valid(), False,
                         "Empty resource_user_select is considered as valid")
        self.assertEqual(self.resource_user_select.data_type, RESOURCE_USER_SELECT,
                         "resource_user_select type is incorrect")
        self.resource_user_select.text_data = { "role": ROLE_FRANCHISE }
        self.assertEqual(self.resource_user_select.is_valid(), True,
                         "Valid resource_user_select is considered as not valid")
        self.assertEqual(self.resource_user_select.role, ROLE_FRANCHISE,
                         "resource_user_select's role doesn't work properly")
        self.resource_user_select.file_data = ['file_name']
        self.assertEqual(self.resource_user_select.is_valid(), False,
                         "Not valid resource_user_select is considered as valid")


