from invoke import Collection

from . import setup, reset, clone, apps


ns = Collection(setup, reset, clone, apps)


ns.configure({
    'base_env_files': [
        'configs/env/common.env',
        'configs/env/heroku.env',
        'configs/env/secret.env'
    ],
    'default_app_label': 'local',
    'apps': {
        'local': {'type': 'local', 'pipeline': 'canada'},
        'dev': {'type': 'heroku', 'name': 'canada-dev', 'pipeline': 'canada'},
#        'prod': {'type': 'heroku', 'name': 'canada', 'confirm': True}
    }
})
