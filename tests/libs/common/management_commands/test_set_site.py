from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class TestSetSiteCommand(TestCase):

    def assert_current_site_domain(self, domain):
        site = Site.objects.get_current()
        if domain != site.domain:
            raise AssertionError(
                '"{}" does not match the current site domain of "{}"'.format(
                    domain,
                    site.domain
                )
            )

    def test_allowed_host(self):
        '''
        ``set_site`` should set the default site to the first allowed
        host from the settings, if not called with a domain
        '''
        test_domain = 'hey-test.com'
        with self.settings(ALLOWED_HOSTS=[test_domain]):
            call_command('set_site')
        self.assert_current_site_domain(test_domain)

    def test_other_domain(self):
        '''
        ``set_site`` should set the defalt site to a domain, if passed in as
        an argument
        '''
        test_domain = 'hey-test.com'
        call_command('set_site', test_domain, verbosity=0)
        self.assert_current_site_domain(test_domain)

    def test_invalid_arguments(self):
        '''
        ``set_site`` should raise a command error when called with > 1 argument
        '''

        with self.assertRaises(CommandError):
            call_command('test_site', '', '', verbosity=0)
