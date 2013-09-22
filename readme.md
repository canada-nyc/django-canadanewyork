[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.png?branch=production)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)

# Depedencies
## Essential
* python 2.7.x
* less and sass for compression: ` npm install --global --production "less" "sass"`

## Recommended
* libmemcached-dev: Mac -> `brew install libmemcached`
  For postgresql database
* Postgresql: Mac -> `brew install postgresql` or [Postgress.app](http://postgresapp.com/).
* foreman: `gem install foreman`
  For managing environmental variables

# Setup
All runtime options are chosen using environmental variables.

The project uses the the `configs/env/*` files to set variables for different
environemnts. Those files are pushed to Heroku and used for local development
so as to consolide the configuration.

It is currently set up to use `foreman` to set environmental variables
from the config files at runtime, when developing locally.

The default environemt variable files that are read by foreman are listed in
`.foreman`. Take a look at those files and what their options are. If you want
to overide any of the options you can change the file. In the future I plan
to allow configuring all options by command line flags as well as
environemental variables.

The only file that is not checked into version control is
`configs/env/secret.evn`. Put any variables in that file that should not be
public. Currently it contains:
* `SECRET_KEY` needed by django to make the application safe.
* `ADMIN_PASSWORD` used by `manage.py clean_db` to create a superuser admin account
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

To use the environental variables defined in the files, which are in turn
defined in `.foreman`, prefex any command with `foreman run`. For example
`foreman run python manage.py runserver`.

# `Makefile`
The `Makefile` is written for the
[fish shell](https://github.com/fish-shell/fish-shell) syntax. If you don't
have fish installed then stay away from it. Also, because I can not get `make`
to run the commands in the current shell environment, I had to hardcode the
python virtualenv path at the top of the makefile. If you do use the makefile
then you will have to modify that for your own python interpreter.

# Initial Data

To wipe static, media, cache, and database
```
foreman run python manage.py clean_db --noinput
```

To import the old wordpres site:
```
foreman run python python manage.py import_wp static/wordpress/.canada.wordpress.*
```

Or if you don't feel like waiting to get all of those images, just
create some factory models.
```
foreman run python manage.py clean_db --noinput --init
```
