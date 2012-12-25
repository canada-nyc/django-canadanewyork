SHELL := /usr/local/bin/fish
heroku:
	heroku plugins:install git://github.com/joelvh/heroku-config.git
	heroku addons:add newrelic:standard
	heroku addons:add redistogo
	heroku addons:add memcachier:dev
	heroku addons:add heroku-postgresql:dev
	heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
	heroku config:add DJANGO_SETTINGS_MODULE="configs.settings.prod" BUILDPACK_URL=git://github.com/saulshanabrook/heroku-buildpack-django.git
	heroku config:push -o
	heroku pg:promote (heroku pg | grep '^===' | sed 's/^=== //g')
	git push heroku master:master
	heroku run 'python manage.py clean_db --no-wipe --no-init'
migrate:
	for app in (python manage.py syncdb | grep - | sed 's/ - //g'); python manage.py schemamigration $app --auto; end
wipe-migrations:
	rm -r {apps,libs}/*/migrations; for app in (python manage.py syncdb | grep '^ . apps\|libs' | sed 's/ > //g' | sed 's/ - //g'); python manage.py schemamigration $app --initial; end
migrate-initial:
	for app in (python manage.py syncdb | grep '^ . apps\|libs' | sed 's/ > //g' | sed 's/ - //g'); python manage.py schemamigration $app --initial; end
