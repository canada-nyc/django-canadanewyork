from django.test import TestCase
from django.test.utils import override_settings

from .models import CKEditorModel
from ...utils import AddAppMixin


@override_settings(CKEDITOR_CLASS='hey')
class CKEditorTest(AddAppMixin, TestCase):
    custom_apps = ('tests.libs.ckeditor',)

    def setUp(self):
        self.model = CKEditorModel.objects.create(html='test')

    def test_as_html_attribute(self):
        self.assertEqual(self.model.html.as_html, '<div class="hey">test</div>\n')
