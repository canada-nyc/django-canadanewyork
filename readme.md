[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.png?branch=production)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)
# Install
```sh
pip install -r requirements/dev.txt
gem install foreman
foreman run python manage.py clean_db
foreman run python manage.py runserver
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
heroku config:push -o --filename config/env/common.env
heroku config:push -o --filename config/env/prod.env
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
for line in (cat configs/env/common.env configs/env/travis.env configs/env/testing.env);
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