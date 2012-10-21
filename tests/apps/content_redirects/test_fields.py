from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
from django.test.utils import override_settings
from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.core.exceptions import ValidationError

from .models import RedirectModel
from .factories import RedirectModelFactory, RedirectModel_2Factory


@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.apps.content_redirects',))
class TestContentRedirects(TestCase):
    def setUp(self):
        loading.cache.loaded = False
        call_command('syncdb')

    def test_save(self):
        _Content = RedirectModelFactory()
        _Redirect = _Content.redirect
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(_Content.old_path, _Redirect.old_path)

    def test_change_old_path(self):
        _Content = RedirectModelFactory()
        _Content.old_path = '/from/another'
        _Content.save()
        _Redirect = _Content.redirect
        self.assertEqual(_Content.old_path, _Redirect.old_path)
        self.assertEqual(1, Redirect.objects.count())

    def test_change_absolute_url(self):
        _Content = RedirectModelFactory()
        _Content.text = 'new text'
        _Content.save()
        _Redirect = _Content.redirect
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(1, Redirect.objects.count())

    def test_remove_old_path(self):
        '''
        Test to make sure that the Redirect deletes itself,
         when the old_path is not set
        '''
        _Content = RedirectModelFactory()
        _Content.old_path = ''
        _Content.save()
        self.assertFalse(Redirect.objects.count())

    def test_recreate(self):
        '''
        Test to make sure that Redirect recreates itself if `from_url`
        is supplied
        '''
        _Content = RedirectModelFactory(old_path='')
        self.assertFalse(Redirect.objects.count())
        _Content.old_path = 'path'
        _Content.save()
        _Redirect = _Content.redirect
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(_Redirect.old_path, _Redirect.old_path)

    def test_multiple_blank_old_path(self):
        '''
        If multiple old_paths are blank, then no error should be raised,
        because they are not conflicting
        '''
        _Content_1 = RedirectModelFactory(old_path='')
        _Content_2 = RedirectModelFactory(old_path='')
        self.assertFalse(Redirect.objects.count())

    def test_conflicting_old_path(self):
        with self.assertRaisesRegexp(ValidationError, 'old_path'):
            _Content_1 = RedirectModelFactory(old_path='path')
            _Content_2 = RedirectModel_2Factory(old_path='path')
