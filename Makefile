SHELL := /usr/local/bin/fish --login

HEROKU_ADDONS="newrelic,heroku-postgresql,pgbackups:auto-month,MEMCACHIER,sentry"
PYTHON="/Users/saul/.virtualenvs/django-canadanewyork/bin/python"

setup-local:
	pip install -r configs/requirements/dev.txt
	gem install foreman travis
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
	echo 'env: configs/env/common.env,configs/env/secret.env,configs/env/dev.env' > .foreman
	mkdir tmp

setup-heroku-dev:
	heroku plugins:install git://github.com/joelvh/heroku-config.git
	heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
	heroku apps:create canada-development --addons $HEROKU_ADDONS
	heroku config:push -o --filename configs/env/common.env
	heroku config:push -o --filename configs/env/heroku.env
	heroku config:push -o --filename configs/env/secret.env
	heroku config:push -o --filename configs/env/dev.env
	heroku config:set 'heroku_app_'(heroku apps:info -s | grep '^name=')

setup-heroku-prod:
	heroku pgbackups:capture --expire
	heroku apps:create canada --no-remote --addons $HEROKU_ADDONS
	heroku pipeline:add canada
	heroku pipeline:promote
	heroku labs:enable user-env-compile --app canada
	heroku config:push -o --filename configs/env/common.env --app canada
	heroku config:push -o --filename configs/env/heroku.env --app canada
	heroku config:push -o --filename configs/env/secret.env --app canada
	heroku config:push -o --filename configs/env/prod.env --app canada
	heroku config:set 'heroku_app_'(heroku apps:info -s --app canada | grep '^name=') --app canada


reset-local:
	foreman run ${PYTHON} manage.py clean_db --noinputpython manage.py import_wp static/wordpress/.canada.wordpress.*
	foreman run ${PYTHON} manage.py set_site 127.0.0.1:8000
	foreman run ${PYTHON} manage.py loaddata configs/fixtures/contact.json"

reset-heroku-dev:
	heroku pg:reset DATABASE_URL --confirm canada-development
	heroku run 'python manage.py clean_db --noinput'
	heroku run 'python manage.py import_wp static/wordpress/.canada.wordpress.*'
	heroku run 'python manage.py set_site "$heroku_app_name".herokuapps.com'
	heroku run 'python manage.py loaddata configs/fixtures/contact.json'

migrate-all:
	for app in (python manage.py syncdb | grep - | sed 's/ - //g');python manage.py schemamigration $app --auto;end

migrate-wipe:
	rm -r {apps,libs}/*/migrations

migrate-init: migrate-wipe
	for app in (python manage.py syncdb | grep '^ . apps\|libs' | sed 's/ > //g' | sed 's/ - //g');python manage.py schemamigration $app --initial;end

travis-encrypt:
	sed '/  global:/q' .travis.yml > .travis.yml.tmp
	mv -f .travis.yml.tmp .travis.yml
	function t_encrypt; echo "    - secret: " $argv >> .travis.yml; end
	for line in (cat configs/env/secret.env | travis encrypt --no-interactive --split); t_encrypt $line; end
	t_encrypt (travis encrypt HEROKU_API_KEY=(heroku auth:token) --no-interactive)
	for line in (cat configs/env/common.env configs/env/travis.env); echo "    - $line" >> '.travis.yml';end


promote-db-local:
	pg_dump -Fc --no-acl --no-owner -h localhost -U saul django_canadanewyork > django_canadanewyork.dump
	foreman run ${PYTHON} manage.py upload_file django_canadanewyork.dump > dump_url.txt
	rm django_canadanewyork.dump
	heroku pgbackups:restore DATABASE (cat dump_url.txt) --confirm canada-development
	rm dump_url.txt
	foreman run ${PYTHON} manage.py delete_file django_canadanewyork.dump
	heroku run 'python manage.py set_site "$$heroku_app_name".herokuapps.com'

promote-db-heroku-dev:
	heroku pgbackups:capture --expire --app canada-development
	heroku pgbackups:restore DATABASE --app canada (heroku pgbackups:url --app canada-development) --confirm canada
	heroku run 'python manage.py set_site "$$heroku_app_name".herokuapps.com' --app canada

promote-code-local:
	git push heroku master

promote-code-heroku-dev:
	heroku pipeline:promote

promote-static-local:
	foreman run ${PYTHON} manage.py clone_bucket (cat configs/env/dev.env | grep AWS_BUCKET | sed 's/AWS_BUCKET=//g') (heroku config:get AWS_BUCKET --app canada-development)

promote-static-heroku-dev:
	heroku run 'python manage.py clone_bucket (heroku config:get AWS_BUCKET --app canada-development) (heroku config:get AWS_BUCKET --app canada)'

promote-all-local: promote-code-local promote-db-local promote-static-local

promote-all-heroku-dev: heroku-promote-static heroku-promote-code heroku-promote-db
