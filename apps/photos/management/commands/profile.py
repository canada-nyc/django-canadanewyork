import time
import cProfile
import pstats

from django.core.management.base import BaseCommand
from django.template import RequestContext, Template
from django.test.client import RequestFactory

from ..utils import use_test_database
from ..dummy_profiling_app.factories import RelatedPhotoFactory


class Command(BaseCommand):
    help = 'Profile photo generation with different settings'

    image_size = 1000
    photo_numbers = [0, 1, 50]

    def handle(self, *args, **options):
        with use_test_database:
            self.render_times()

    def render_times(self):
        for count in self.photo_numbers:
            print count
            print 'Generation'
            photo_object, seconds = self.create_photos(count)
            print seconds
            print 'First hit'
            seconds = self.render_photo(photo_object)
            print seconds
            print 'Second hit'
            seconds = self.render_photo(photo_object)
            print seconds

    def render_photo(self, photo_object):
        context = RequestContext(
            RequestFactory().request(),
            {'object': photo_object}
        )
        template = Template('''
{% extends "base.html" %}
{% block body %}
{% include "base/photos.html" with photos=object.photos.all id=object.id %}
{% endblock %}
        ''')
        pr = cProfile.Profile(builtins=False)
        pr.enable()
        start_time = time.time()
        template.render(context)
        end_time = time.time()
        pr.disable()
        ps = pstats.Stats(pr)
        ps.sort_stats('cumtime')
        #ps.print_stats(20)
        return end_time - start_time

    def create_photos(self, n):
        start_time = time.time()
        photo_object = RelatedPhotoFactory(
            photos__n=n,
            photos__image__size=self.image_size
        )
        end_time = time.time()
        return photo_object, end_time - start_time
