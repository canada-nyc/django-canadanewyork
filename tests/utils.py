import StringIO
from datetime import date
import os
import base64
import json
import httplib
import sys
import time
import random

from PIL import Image
from factory.fuzzy import BaseFuzzyAttribute
from selenium import webdriver

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading
from django.test import LiveServerTestCase


class Selenium2OnSauce(LiveServerTestCase):
    def setUp(self):
        if not settings.SELENIUM:
            self.skitTest('Selenium not enabled in settings')
        desired_capabilities = webdriver.DesiredCapabilities.CHROME
        desired_capabilities['version'] = ''
        desired_capabilities['platform'] = "OS X 10.8"
        desired_capabilities['public'] = 'public'
        desired_capabilities['name'] = str(self.id())
        if 'TRAVIS_JOB_NUMBER' in os.environ:
            desired_capabilities['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
        if 'TRAVIS_BUILD_NUMBER' in os.environ:
            desired_capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
            desired_capabilities['tags'] = ['CI']
        else:
            desired_capabilities['build'] = 'local ' + str(time.time())
        self.sauce_username = os.environ['SAUCE_USERNAME']
        self.sauce_key = os.environ['SAUCE_ACCESS_KEY']
        command_executor = "http://{}:{}@localhost:4445/wd/hub".format(
            self.sauce_username,
            self.sauce_key
        )
        self.driver = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor=command_executor
        )
        self.jobid = self.driver.session_id
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.quit()
        self._report_test_result()

    def _report_test_result(self):
        base64string = base64.encodestring(
            '{}:{}'.format(self.sauce_username, self.sauce_key)
        )[:-1]
        result = json.dumps({'passed': sys.exc_info() == (None, None, None)})
        connection = httplib.HTTPConnection("saucelabs.com")
        connection.request(
            'PUT',
            '/rest/v1/{}/jobs/{}'.format(self.sauce_username, self.jobid),
            result,
            headers={"Authorization": "Basic " + base64string})
        result = connection.getresponse()
        return result.status == 200


def django_image(name, size=200, color='red'):
    thumb = Image.new('RGB', (size, size,), color)

    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    return InMemoryUploadedFile(thumb_io, None, name, 'image/jpeg', thumb_io.len, None)


class AddAppMixin(object):
    custom_apps = ()

    def _pre_setup(self):
        # Add the models to the db.
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        settings.INSTALLED_APPS += self.custom_apps
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, verbosity=0, migrate=False)
        # Call the original method that does the fixtures etc.
        super(AddAppMixin, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method.
        super(AddAppMixin, self)._post_teardown()
        # Restore the settings.
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False


def random_date(start_date=date(2005, 1, 1), end_date=date.today()):
    return date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))


class FuzzyDate(BaseFuzzyAttribute):
    def __init__(self, start_date=date(2005, 1, 1), end_date=date.today(), **kwargs):
        super(FuzzyDate, self).__init__(**kwargs)
        self.start_date = start_date.toordinal()
        self.end_date = end_date.toordinal()

    def fuzz(self):
        return date.fromordinal(random.randint(self.start_date, self.end_date))
