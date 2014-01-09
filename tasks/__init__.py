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
        'local': {
            'type': 'local',
        },
        'dev': {
            'type': 'heroku',
            'name': 'canada-development',
            'env_file': 'configs/env/heroku-dev.env',
        },
        'prod': {
            'type': 'heroku',
            'confirm': True,
            'name': 'canada',
            'env_file': 'configs/env/heroku-prod.env',
        }
    }
})
