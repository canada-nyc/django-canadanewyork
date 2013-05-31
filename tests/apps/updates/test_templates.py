from time import time
import cProfile
import pstats

from django_webtest import WebTest
from django.core.urlresolvers import reverse

from .factories import UpdateFactory


class UpdateListTest(WebTest):
    def test_reverse(self):
        self.app.get(
            reverse('update-list')
        )

    def test_nav_click(self):
        update_list = self.app.get(
            reverse('update-list')
        )
        update_list.click(
            'Updates',
            href=reverse('update-list')
        )

    def test_click_indivual(self):
        Update = UpdateFactory()
        update_list = self.app.get(
            reverse('update-list')
        )
        update_list.click(
            href=reverse('update-detail', kwargs={'pk': Update.pk})
        )


class UpdateRenderSpeedTest(WebTest):
    def test_list(self):
        print 'Getting update page initially to cache javscript'
        self.app.get(reverse('update-list'))
        number_of_updates = 40
        print 'Creating {} Test Updates'.format(str(number_of_updates))
        start_time = time()
        for _ in range(number_of_updates):
            UpdateFactory(photos__n=1)
        print 'It took {} seconds'.format(time() - start_time)
        print 'Accessing update list for the first time'
        start_time = time()
        pr = cProfile.Profile(subcalls=True, builtins=False)
        pr.enable()
        self.app.get(reverse('update-list'))
        pr.disable()
        print 'It took {} seconds'.format(time() - start_time)
        ps = pstats.Stats(pr)
        ps.sort_stats('cumtime')
        ps.print_stats(.05)
        print 'Trying to access again'
        start_time = time()
        pr = cProfile.Profile(subcalls=True, builtins=False)
        pr.enable()
        self.app.get(reverse('update-list'))
        pr.disable()
        print 'It took {} seconds'.format(time() - start_time)
        ps = pstats.Stats(pr)
        ps.sort_stats('cumtime')
        ps.print_stats(.05)


class UpdateDetailTest(WebTest):
    def test_description(self):
        Update = UpdateFactory(description='description')
        update_detail = self.app.get(Update.get_absolute_url())
        self.assertIn(Update.description, update_detail)
