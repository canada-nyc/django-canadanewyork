from .common import *


############
# SECURITY #
############
ALLOWED_HOSTS = (
    "{HEROKU_APP_NAME}.herokuapp.com".format(
        HEROKU_APP_NAME=os.environ.get('heroku_app_name'),
    ),
)
