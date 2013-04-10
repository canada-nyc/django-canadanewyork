[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.png?branch=production)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)

# Local Install
## Depedencies
1. libmemcached-dev: On a mac `brew install libmemcached`
2. Postgresql (not required but preferable for consistancy): Mac users try or `brew install postgresql`
[Postgress.app](http://postgresapp.com/).
3. foreman: `gem install foreman`
4. less and uglify-js for compression: `npm install --global --production "less" "git://github.com/mishoo/UglifyJS2.git#3bd7ca9961125b39dcd54d2182cb72bd1ca6006e"`

## Setup
A number of environmental variables need to be set. I use foreman to run my
app with the required variables. So first make foreman use the config
files provided with variables
`echo 'env: configs/env/common.env,configs/env/secret.env,configs/env/dev.env,configs/env/local.env' > .foreman`

Then add these variables to `configs/env/secret.env`:

```
DATABASE_URL=
SECRET_KEY=
ADMIN_PASSWORD=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

The `DATABASE_URL` can be any format that [dj-database-url](https://github.com/kennethreitz/dj-database-url) can handle.

You can also change the `AWS_BUCKET` which is in `configs/env/dev.env`.

Then install all requirements, preferably in a virtualenv
`pip install -r configs/requirements/dev.txt --use-mirrors`

## Initial Data

Then sync the static and import the old wordpress site:
```
foreman run python manage.py clean_db --noinput
foreman run python python manage.py import_wp static/wordpress/.canada.wordpress.*
```
Or if you don't feel like waiting to get all of those images, just
create some factory models.
```
foreman run python manage.py clean_db --noinput --init
```

Then set the site and contact pages.
```
foreman run python manage.py set_site 127.0.0.1:8000
foreman run python manage.py loaddata configs/fixtures/contact.json
```

Finally run the local server
```
foreman run python manage.py runserver
```
