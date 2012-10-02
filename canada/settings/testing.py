import os

from .django import RelPath


class Testing(RelPath):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

    @property
    def TEST_DISCOVER_TOP_LEVEL(self):
        return super(Testing, self).rel_path('..')

    @property
    def TEST_DISCOVER_ROOT(self):
        return os.path.join(self.TEST_DISCOVER_TOP_LEVEL, 'tests')

    SOUTH_TESTS_MIGRATE = False
