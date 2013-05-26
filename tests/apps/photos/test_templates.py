import time

from memcacheify import memcacheify

from django.test import TestCase
from django.template import RequestContext, Template
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.conf import settings

from libs.common.utils import rel_path
from .factories import TestPhotoFactory
from ...utils import AddAppMixin


LOCAL_STORAGE = {
    'STATICFILES_STORAGE': 'django.core.files.storage.FileSystemStorage',
    'COMPRESS_STORAGE': 'django.core.files.storage.FileSystemStorage',
    'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
    'STATIC_URL': '/static/',
    'STATIC_ROOT': rel_path('tmp_testing/static'),
    'MEDIA_ROOT': rel_path('tmp_testing/media'),
    'MEDIA_URL': '/media/',
}

REMOTE_STORAGE = {
    'STATICFILES_STORAGE': 'storages.backends.s3boto.S3BotoStorage',
    'COMPRESS_STORAGE': 'storages.backends.s3boto.S3BotoStorage',
    'DEFAULT_FILE_STORAGE': 'storages.backends.s3boto.S3BotoStorage',
    'STATIC_URL': 'http://{}/'.format(settings.AWS_S3_CUSTOM_DOMAIN),
    'COMPRESS_URL': 'http://{}/'.format(settings.AWS_S3_CUSTOM_DOMAIN),
    'AWS_S3_CUSTOM_DOMAIN': 'assets-testing.canadanewyork.com',
    'AWS_STORAGE_BUCKET_NAME': 'assets-testing.canadanewyork.com',
}

NO_CACHE = {
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
}

MEMCACHE = {
    'CACHES': memcacheify(),
}


class Timer(object):
    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, type, value, traceback):
        self.__finish = time.time()

    def duration_in_seconds(self):
        return self.__finish - self.__start


class TimingTest(AddAppMixin, TestCase):
    custom_apps = ('tests.apps.photos',)

    def time_photos(self, test_object):
        timer = Timer()
        context = RequestContext(RequestFactory().request(), {'object': test_object})
        template = Template('''
            {% extends "base.html" %}
            {% block body %}
            {% include "base/photos.html" with photos=object.photos.all id=object.id %}
            {% endblock %}
        ''')
        with timer:
            template.render(context)
        return timer.duration_in_seconds()

    def photo_object(self, number_photos):
        return TestPhotoFactory(photos__n=number_photos, photos__image__size=1000)

    def slope(self, points):
        slopes = []
        for index, point in enumerate(points[1:]):
            previous_point = points[index - 1]
            rise = point[1] - previous_point[1]
            run = point[0] - previous_point[0]
            slopes.append(rise / run)
        return float(sum(slopes)) / len(slopes)

    def run_creation(self):
        first_hit_data = []
        second_hit_data = []
        for number in range(0, 4, 2):
            object = self.photo_object(number)
            first_hit_data.append([float(number), self.time_photos(object)])
            print '{} first hit: {}'.format(*first_hit_data[-1])
            second_hit_data.append([float(number), self.time_photos(object)])
            print '{} second hit: {}'.format(*first_hit_data[-1])
        print '{} seconds per photo on first hit'.format(self.slope(first_hit_data))
        print '{} seconds per photo on second hit'.format(self.slope(second_hit_data))

    def clear_local_storage()

    @override_settings(**dict(LOCAL_STORAGE.items() + NO_CACHE.items()))
    def test_local(self):
        print 'Using local storage, no cache'
        self.clear_local_storage()
        self.run_creation()

    @override_settings(**dict(REMOTE_STORAGE.items() + NO_CACHE.items()))
    def test_remote(self):
        print 'using S3 storage, no cache'
        self.run_creation()

    @override_settings(**dict(LOCAL_STORAGE.items() + MEMCACHE.items()))
    def test_local_cache(self):
        print 'Using local storage, yes cache'
        self.run_creation()

    @override_settings(**dict(REMOTE_STORAGE.items() + MEMCACHE.items()))
    def test_remote_cache(self):
        print 'using S3 storage, yes cache'
        self.run_creation()
