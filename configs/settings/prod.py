from .common import *


############
# SECURITY #
############
ALLOWED_HOSTS = (
    "{HEROKU_APP_NAME}.herokuapp.com".format(
        HEROKU_APP_NAME=get_env_variable('heroku_app_name'),
    ),
)
