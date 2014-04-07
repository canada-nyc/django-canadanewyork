import pickle

from django.test import TestCase
from django.test.utils import override_settings
from django.template import Context, Template

from .models import CKEditorModel
from ...utils import AddAppMixin


@override_settings(CKEDITOR_CLASS='hey')
class CKEditorTest(AddAppMixin, TestCase):
    custom_apps = ('tests.libs.ckeditor',)

    def setUp(self):
        self.model = CKEditorModel.objects.create(html='<p>test</p>')
        self.target_html = '<div class="hey"><p>test</p></div>\n'

    def test_as_html_attribute(self):
        self.assertEqual(self.model.html.as_html, self.target_html)

    def test_blank_is_not_none(self):
        '''
        Make sure when there is no string that it returns an empty string and
        not None
        '''
        self.model.html = ''
        self.target_html = '<div class="hey"></div>\n'

        self.assertEqual(self.model.html.as_html, self.target_html)

    def test_no_save_is_not_save(self):
        '''
        Make sure when there is not a saved string at first.
        '''
        self.model = CKEditorModel.objects.create()
        self.target_html = '<div class="hey"></div>\n'

        self.assertEqual(self.model.html.as_html, self.target_html)

    def test_wont_escape_in_template(self):
        rendered = Template('{{ model.html.as_html }}').render(
            Context({'model': self.model})
        )

        self.assertEqual(rendered, self.target_html)

    def test_pickle(self):
        pickle.dumps(self.model)
