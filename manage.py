#!/usr/bin/env python
import os
import sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.canada")
os.environ.setdefault('DJANGO_CONFIGURATION', 'LocalSettings')

if __name__ == "__main__":
    from configurations.management import execute_from_command_line
    execute_from_command_line(sys.argv)

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
