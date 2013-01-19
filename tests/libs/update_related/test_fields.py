from django.test import TestCase
from django.db import IntegrityError

from .models import RedirectModel, RedirectSlugifyModel
from ...common.base_test import AddAppMixin
from libs.redirects.models import Redirect


class TestContentRedirects(AddAppMixin, TestCase):
    custom_apps = ('tests.libs.update_related',)

    def test_save(self):
        RedirectModel.objects.create(old_path='old')

        _Content = RedirectModel.objects.all()[0]
        _Redirect = _Content.redirect
        self.assertTrue(_Redirect)
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(_Content.old_path, _Redirect.old_path)

    def test_change_old_path(self):
        _Content = RedirectModel.objects.create(old_path='old')

        _Content = RedirectModel.objects.all()[0]
        self.assertEqual(_Content.old_path, _Content.redirect.old_path)

        _Content.old_path = '/from/another'
        _Content.save()

        _Content = RedirectModel.objects.all()[0]
        _Redirect = _Content.redirect
        self.assertEqual(_Content.old_path, _Redirect.old_path)
        self.assertEqual(1, Redirect.objects.count())

    def test_change_absolute_url(self):
        _Content = RedirectModel.objects.create(old_path='old')

        _Content = RedirectModel.objects.all()[0]
        _Content.text = 'new text'
        _Content.save()

        _Content = RedirectModel.objects.all()[0]
        _Redirect = _Content.redirect
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(1, Redirect.objects.count())

    # def test_remove_old_path(self):
    #     '''
    #     Test to make sure that the Redirect deletes itself,
    #      when the old_path is not set
    #     '''
    #     _Content = RedirectModel.objects.create(old_path='old')
    #     _Content = RedirectModel.objects.all()[0]
    #     _Content.old_path = ''
    #     _Content.save()
    #     self.assertFalse(Redirect.objects.count())

    # def test_delete_model(self):
    #     '''
    #     Makes sure the redirect gets deleted after the model does
    #     '''
    #     _Content = RedirectModel.objects.create(old_path='old')
    #     _Content = RedirectModel.objects.all()[0]
    #     _Content.delete()
    #     self.assertFalse(Redirect.objects.count())

    def test_recreate(self):
        '''
        Test to make sure that Redirect recreates itself if `from_url`
        is supplied
        '''
        _Content = RedirectModel.objects.create(old_path='')
        self.assertFalse(Redirect.objects.count())

        _Content = RedirectModel.objects.all()[0]
        _Content.old_path = 'path'
        _Content.save()

        _Content = RedirectModel.objects.all()[0]
        _Redirect = _Content.redirect
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(_Redirect.old_path, _Redirect.old_path)

    def test_multiple_blank_old_path(self):
        '''
        If multiple old_paths are blank, then no error should be raised,
        because they are not conflicting
        '''
        RedirectModel.objects.create(old_path='')
        RedirectModel.objects.create(old_path='')
        self.assertFalse(Redirect.objects.count())

    def test_conflicting_old_path(self):
        with self.assertRaisesRegexp(IntegrityError, 'path'):
            RedirectModel.objects.create(old_path='path')
            RedirectModel.objects.create(old_path='path')

    def test_slugify_happens_first(self):
        _Content = RedirectSlugifyModel.objects.create(old_path='path')

        _Content = RedirectSlugifyModel.objects.all()[0]
        _Redirect = _Content.redirect
        self.assertTrue(_Redirect)
        self.assertEqual(_Content.get_absolute_url(), _Redirect.new_path)
        self.assertEqual(_Content.old_path, _Redirect.old_path)
