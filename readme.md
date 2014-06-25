[![Stories in Ready](https://badge.waffle.io/saulshanabrook/django-canadanewyork.png?label=ready&title=Ready)](https://waffle.io/saulshanabrook/django-canadanewyork)
[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.png?branch=production)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)
[![Requirements Status](https://requires.io/github/saulshanabrook/django-canadanewyork/requirements.png?branch=master)](https://requires.io/github/saulshanabrook/django-canadanewyork/requirements/?branch=master)


# Depedencies
## Essential
* python 2.7.x

## Recommended
* libmemcached-dev: Mac -> `brew install libmemcached`
  For postgresql database
* Postgresql: Mac -> `brew install postgresql``
* foreman: `gem install foreman`
  For managing environmental variables
* Less: `npm install --global --production less`
  For compressing static
* Sass: `gem install sass`
  For compressing Magnific Popup static

# Setup
All runtime options are chosen using environmental variables.

The project uses the the `configs/env/*` files to set variables for different
environemnts. Those files are pushed to Heroku and used for local development
so as to consolide the configuration.

It is currently set up to use `foreman` to set environmental variables
from the config files at runtime, when developing locally.

The default environemt variable files that are read by foreman are listed in
`.foreman`. Take a look at those files and what their options are. If you want
to overide any of the options you can change `configs/env/local.env`.

The only file that is not checked into version control is
`configs/env/secret.evn`. Put any variables in that file that should not be
public. Currently it contains:
* `SECRET_KEY` needed by django to make the application safe.
* `ADMIN_USERNAME` used by `manage.py clean_db` to create a superuser admin account
* `ADMIN_PASSWORD` used by `manage.py clean_db` to create a superuser admin account
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

To use the environental variables defined in the files, which are in turn
defined in `.foreman`, prefex any command with `foreman run`. For example
`foreman run python manage.py runserver`.

# Running Tasks
There are two ways to run one off tasks on any app. The first is through
`manage.py` commands. These are meant for any task that can be executed only
through Python on one specific instance of the app. For instance, creating default
user permssions or importing the existing database file.

The other is through the `inv[oke]` command. This replace the previous `make`
command in running command that involve multiple apps, or that do not only use
Python. It is a nice wrapper around any tasks that need to be automated. It
while the management commands are meant to be run on any instance, the invoke
commands should only be run locally. To see all of the commands run
`inv --list`. Most commands take one or more `app_label`s. This specifies which
instance to run the command on, local, dev, or prod.
