heroku addons:add newrelic:standard
heroku addons:add redistogo
heroku addons:add memcachier:dev
heroku addons:add heroku-postgresql:dev
heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
heroku config:add DJANGO_SETTINGS_MODULE=canada.settings.prod SECRET_KEY='fa3rsdgaxczx' AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
heroku run './manage.py syncdb --noinput && ./manage.py migrate'
