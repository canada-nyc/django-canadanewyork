[![Stories in Ready](https://badge.waffle.io/saulshanabrook/django-canadanewyork.png?label=ready&title=Ready)](https://waffle.io/saulshanabrook/django-canadanewyork)
[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.svg?branch=master)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)
[![Code Health](https://landscape.io/github/saulshanabrook/django-canadanewyork/master/landscape.svg?style=flat)](https://landscape.io/github/saulshanabrook/django-canadanewyork/master)
[![Requirements Status](https://requires.io/github/saulshanabrook/django-canadanewyork/requirements.png?branch=master)](https://requires.io/github/saulshanabrook/django-canadanewyork/requirements/?branch=master)
[![Dependency Status](https://gemnasium.com/saulshanabrook/django-canadanewyork.svg)](https://gemnasium.com/saulshanabrook/django-canadanewyork)

# Setup
All runtime options are chosen using environmental variables.

The project uses the the `configs/env/*` files to set variables for different
environemnts. Those files are pushed to Heroku and used for local development
so as to consolide the configuration.

The only file that is not checked into version control is
`configs/env/secret.evn`. Put any variables in that file that should not be
public. Currently it contains:
* `SECRET_KEY` needed by django to make the application safe.
* `ADMIN_USERNAME` used by `manage.py clean_db` to create a superuser admin account
* `ADMIN_PASSWORD` used by `manage.py clean_db` to create a superuser admin account
* `AWS_ACCESS_KEY_ID` only needed if using s3 storage
* `AWS_SECRET_ACCESS_KEY` only needed if using s3 storage

# Local
All local development is done through docker.

To start the developmente server use `docker-compose up`

If you wanna run the tests, do `docker-compose run web python manage.py test`.

# Running Tasks
There are two ways to run one off tasks on any app. The first is through
`manage.py` commands. These are meant for any task that can be executed only
through Python on one specific instance of the app. For instance, creating default
user permssions or importing the existing database file.

We run these through docker

The other is through the `inv[oke]` command. This replace the previous `make`
command in running command that involve multiple apps, or that do not only use
Python. It is a nice wrapper around any tasks that need to be automated. It
while the management commands are meant to be run on any instance, the invoke
commands should only be run locally. To see all of the commands run
`inv --list`. Most commands take one or more `app_label`s. This specifies which
instance to run the command on, local, dev, or prod.
