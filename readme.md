[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.png?branch=production)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)

# Development

## Install
```sh
pip install -r requirements/dev.txt
gem install foreman
# Install NPM if you don't have it installed
# Tutorial on installing http://stackoverflow.com/questions/8986709/how-to-install-lessc-and-nodejs-in-a-python-virtualenv
# On homebrew do `brew install nodejs`
npm install -g less

echo 'SECRET_KEY=<long and random>
EMAIL_HOST_PASSWORD=<only used for sending batch email, required in settings>
ADMIN_PASSWORD=<default password for admin user>
ADMIN_EMAIL=<email for admin user>
AWS_ACCESS_KEY_ID=<for storages>
AWS_SECRET_ACCESS_KEY=
HEROKU_API_KEY=<for use in controlling worker with email>
SENTRY_DSN=<for logging>
' > configs/env/secret.env
mkdir tmp

# for factory data
foreman run python manage.py clean_db --init --env=configs/env/common.env,configs/env/secret.env
# or for importing from wordpress
foreman run python manage.py import_wp static/wordpress/.canada.wordpress.* --env=configs/env/common.env,configs/env/secret.env
python manage.py set_site 127.0.0.1:8000
python manage.py runserver
```

### Wipe
```sh
# wipes either S3 or local storage, depending on current settings
# also wipes database
foreman run python manage.py clean_db --env=configs/env/common.env,configs/env/secret.env
```


## Schema

### Migrate

```sh
#!/usr/bin/env fish
for app in (python manage.py syncdb | grep - | sed 's/ - //g');
    python manage.py schemamigration $app --auto;
end
```
### Wipe Migrations

```sh
#!/usr/bin/env fish
rm -r {apps,libs}/*/migrations
```

### Initial Migrations
```sh
#!/usr/bin/env fish
for app in (python manage.py syncdb | grep '^ . apps\|libs' | sed 's/ > //g' | sed 's/ - //g');
    python manage.py schemamigration $app --initial;
end
```


## Encrypt Variables for Travis
```sh
#!/usr/bin/env fish
gem install travis

sed '/  global:/q' .travis.yml > .travis.yml.tmp
mv -f .travis.yml.tmp .travis.yml


cat configs/env/secret.env | travis encrypt --no-interactive --add --split
travis encrypt HEROKU_API_KEY=(heroku auth:token) --no-interactive --add

for line in (cat configs/env/common.env configs/env/travis.env);
    echo "    - $line" >> '.travis.yml';
end

```


# Production (Heroku)

## Create App

### Create Development
```sh
#!/usr/bin/env fish
heroku apps:create canada-development --addons newrelic:standard,redistogo,memcache,heroku-postgresql:dev,pgbackups
heroku plugins:install git://github.com/joelvh/heroku-config.git
heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
heroku config:push -o --filename configs/env/common.env
heroku config:push -o --filename configs/env/heroku.env
heroku config:push -o --filename configs/env/secret.env
heroku config:push -o --filename configs/env/dev.env
heroku config:set 'heroku_app_'(heroku apps:info -s | grep '^name=')
git push heroku master
heroku run 'python manage.py clean_db --noinput'
heroku run 'python manage.py import_wp static/wordpress/.canada.wordpress.*'
heroku run 'python manage.py set_site "$heroku_app_name".herokuapps.com'
```

### Create Production
```sh
#!/usr/bin/env fish
heroku pgbackups:capture --expire
heroku apps:create canada --no-remote --addons newrelic:standard,redistogo,memcache,heroku-postgresql:dev,pgbackups
heroku pipeline:add canada
heroku pipeline:promote
heroku labs:enable user-env-compile --app canada
heroku config:push -o --filename configs/env/common.env --app canada
heroku config:push -o --filename configs/env/heroku.env --app canada
heroku config:push -o --filename configs/env/secret.env --app canada
heroku config:push -o --filename configs/env/prod.env --app canada
heroku config:set 'heroku_app_'(heroku apps:info -s --app canada | grep '^name=') --app canada
heroku pgbackups:restore DATABASE --app canada (heroku pgbackups:url --app canada-development) --confirm canada
heroku run 'python manage.py set_site "$heroku_app_name".herokuapps.com' --app canada
```

## Promotion
### DB
```sh
heroku pgbackups:capture --expire --app canada-development
heroku pgbackups:restore DATABASE --app canada (heroku pgbackups:url --app canada-development) --confirm canada
```
### Code
```sh
heroku pipeline:promote
```


## Wipe

### Development
```sh
#!/usr/bin/env fish
heroku pg:reset DATABASE_URL --confirm canada-development
heroku run 'python manage.py clean_db --noinput' --app canada-development
# --no-wipe-static for not deleting all static
heroku run 'python manage.py import_wp static/wordpress/.canada.wordpress.*' --app canada-development
```

### Production
```sh
heroku run 'python manage.py clean_db --noinput' --app canada
heroku pgbackups:capture --expire --app canada-development
heroku pgbackups:restore DATABASE --app canada (heroku pgbackups:url --app canada-development) --confirm canada
heroku run 'python manage.py set_site "$heroku_app_name".herokuapps.com' --app canada
```
