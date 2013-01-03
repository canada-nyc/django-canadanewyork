[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.png?branch=production)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)
# Install
```sh
pip install -r requirements/dev.txt
gem install foreman
# Install NPM if you don't have it installed
# Tutorial on installing http://stackoverflow.com/questions/8986709/how-to-install-lessc-and-nodejs-in-a-python-virtualenv
# On homebrew do `brew install nodejs`
npm install -g less

echo 'SECRET_KEY=<long and random>
EMAIL_HOST_PASSWORD=<only used for sending batch email, required in settings>
ADMIN_USERNAME=<for automatic admin creation>
ADMIN_PASSWORD=<default password>
ADMIN_EMAIL=
' > configs/env/common.env
mkdir tmp
foreman -e configs/env/common.env run python manage.py clean_db --init
python manage.py runserver
```
# Deploy

## Heroku
```sh
#!/usr/bin/env fish
heroku plugins:install git://github.com/joelvh/heroku-config.git
heroku addons:add newrelic:standard
heroku addons:add redistogo
heroku addons:add memcachier:dev
heroku addons:add heroku-postgresql:dev
heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
heroku config:push -o --filename configs/env/common.env
heroku config:push -o --filename configs/env/heroku.env
heroku config:push -o --filename configs/env/prod.env
heroku pg:promote (heroku pg | grep '^===' | sed 's/^=== //g')
git push heroku master
heroku run 'python manage.py clean_db'
```

## Travis
```sh
#!/usr/bin/env fish
gem install specific_install
gem specific_install -l https://github.com/saulshanabrook/travis-cli.git
sed -i '' '/^    - secure: /d'  .travis.yml
for line in (cat configs/env/common.env configs/env/travis.env);
    travis encrypt saulshanabrook/django-canadanewyork $line >> '.travis.yml';
end
travis encrypt saulshanabrook/django-canadanewyork HEROKU_API_KEY=(heroku auth:token) >> '.travis.yml'
```

# Schema

## Migrate

```sh
#!/usr/bin/env fish
for app in (python manage.py syncdb | grep - | sed 's/ - //g');
    python manage.py schemamigration $app --auto;
end
```
## Wipe Migrations

```sh
#!/usr/bin/env fish
rm -r {apps,libs}/*/migrations
```

## Initial Migrations
```sh
#!/usr/bin/env fish
for app in (python manage.py syncdb | grep '^ . apps\|libs' | sed 's/ > //g' | sed 's/ - //g');
    python manage.py schemamigration $app --initial;
end
```
