from django.conf import settings
from django.test.utils import override_settings
from django.test.simple import DjangoTestSuiteRunner
from django.core.management import call_command
from django.db.models import loading


class extra_override_settings(override_settings):
    """
    Allows support in override settings for a custom pre_function to be run
    after the settings are changed.
    """
    def __init__(self, pre_function, post_function=None, **kwargs):
        self.pre_function = pre_function
        self.post_function = post_function
        super(extra_override_settings, self).__init__(**kwargs)

    def enable(self):
        super(extra_override_settings, self).enable()
        self.pre_function()

    def disable(self):
        super(extra_override_settings, self).disable()
        if self.post_function:
            self.post_function()


def set_new_app():
    global old_config
    old_config = DjangoTestSuiteRunner().setup_databases()
    loading.cache.loaded = False
    call_command('syncdb', interactive=False, verbosity=0, migrate=False)


def remove_new_app():
    loading.cache.loaded = False
    DjangoTestSuiteRunner().teardown_databases(old_config)

testing_apps = [app for app in settings.INSTALLED_APPS if app != 'south']
testing_apps.append('apps.photos.management.dummy_profiling_app')
use_test_database = extra_override_settings(
    set_new_app,
    remove_new_app,
    INSTALLED_APPS=testing_apps
)
