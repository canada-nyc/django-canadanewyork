from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
from django.test.utils import override_settings
from django.conf import settings
from django.contrib.redirects.models import Redirect

from apps.model_redirects.models import ContentRedirectModel
from .models import ContentRedirect


@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.apps.content_redirects',))
class TestContentRedirect(TestCase):
    def setUp(self):
        loading.cache.loaded = False
        call_command('syncdb')

    def test_save(self):
        _Content = ContentRedirectModel.objects.create(text='test text',
                                                       old_path='/from/here')
        _ContentRedirect = ContentRedirect.objects.get(object=content)
        _Redirect = _ContentRedirect.redirect
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(content.old_path, _Redirect.old_path)

    def test_change_old_path(self):
        _Content.old_path = '/from/another'
        _Content.save()
        self.assertEqual(_Content.old_path, _Redirect.old_path)

    def test_change_absolute_url(self):
        _Content.text = 'new text'
        _Content.save()
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)

    def test_remove_old_path(self):
        '''
        Test to make sure that ContentRedirect deletes itself and the redirect
        model, when the old_path is not set
        '''
        _Content.old_path = ''
        _Content
        self.assertFalse(ContentRedirect.objects.count() or
                         Redirect.objects.count())

    def test_recreate(self):
        _Content = ContentRedirectModel.objects.create(text='test text',
                                                       old_path='/from/here')
        _ContentRedirect = ContentRedirect.objects.get(object=content)
        _Redirect = _ContentRedirect.redirect
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(content.old_path, _Redirect.old_path)

    def te      st_conflicting_old_path(self):
