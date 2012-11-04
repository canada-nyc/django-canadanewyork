SHELL := /usr/local/bin/fish
heroku:
	heroku plugins:install git://github.com/joelvh/heroku-config.git
	heroku addons:add newrelic:standard
	heroku addons:add redistogo
	heroku addons:add memcachier:dev
	heroku addons:add heroku-postgresql:dev
	heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
	heroku config:add DJANGO_CONFIGURATION=ProductionSettings BUILDPACK_URL=git://github.com/saulshanabrook/heroku-buildpack-django.git
	heroku config:push -o
	heroku pg:promote (heroku pg | grep '^===' | sed 's/^=== //g')
	git push heroku master:master
	heroku run 'python manage.py clean_db --no-wipe'
