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
ADMIN_PASSWORD=<default password for admin user>
ADMIN_EMAIL=<email for admin user>' > configs/env/secret.env
mkdir tmp

# for factory data
foreman run python manage.py clean_db --init --env=configs/env/common.env,configs/env/secret.env
# or for importing from wordpress
foreman run python manage.py import_wp static/wordpress/.canada.wordpress.* --env=configs/env/common.env,configs/env/secret.env
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
heroku config:push -o --filename configs/env/secret.env
heroku config:push -o --filename configs/env/prod.env
heroku pg:promote (heroku pg | grep '^===' | sed 's/^=== //g')
git push heroku master
heroku run 'python manage.py clean_db'
heroku run 'python manage.py import_wp static/wordpress/.canada.wordpress.*'
```

## Travis
```sh
#!/usr/bin/env fish
gem install travis

sed '/  global:/q' .travis.yml | cat | tee .travis.yml

function t_encrypt
    echo "    - secret: "(travis encrypt --no-interactive $argv)
end

function t_var
    echo "    - $argv"
end

for line in (cat configs/env/secret.env);
    t_encrypt $line >> '.travis.yml';
end
for line in (cat configs/env/common.env configs/env/travis.env);
    t_var $line >> '.travis.yml';
end

t_encrypt HEROKU_API_KEY=(heroku auth:token) >> '.travis.yml'
```

# Wiping
```sh
# wipes either S3 or local storage, depending on current settings
# also wipes database
foreman run python manage.py clean_db --env=configs/env/common.env,configs/env/secret.env
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
