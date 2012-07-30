#!/usr/bin/env python
import os
import sys

DJANGO_SETTINGS_MODULE = "canada.settings.dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

if __name__ == "__main__":

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
