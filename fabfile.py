#!/usr/bin/env python
from fabric.api import *


@task(alias='run')
def run_local(debug=False):
    if debug:
        local('python manage.py runserver_plus')
    local('foreman start -e .env_local')
