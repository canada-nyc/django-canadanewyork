import os


if os.getenv('production_setting') == 'Heroku':
    from canada.settings.remote import *
else:
    from canada.settings.local import *

TEMPLATE_DEBUG = DEBUG
