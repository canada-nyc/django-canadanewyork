SHELL := /usr/local/bin/fish --login

PYTHON=/Users/saul/.virtualenvs/django-canadanewyork/bin/python
MANAGE=foreman run ${PYTHON} manage.py

HEROKU_DEV_NAME="canada-development"
HEROKU_PROD_NAME="canada"


run-local-newrelic:
	foreman run newrelic-admin run-program gunicorn --graceful-timeout 600 wsgi:application

setup-local:
	pip install -r configs/requirements/dev.txt
	gem install foreman travis
	# Install NPM if you don't have it installed
	# Tutorial on installing http://stackoverflow.com/questions/8986709/how-to-install-lessc-and-nodejs-in-a-python-virtualenv
	# On homebrew do `brew install nodejs`
	npm install -g less
	mkdir tmp

setup-heroku:
	heroku plugins:install git://github.com/rainforestapp/heroku.json.git
	heroku plugins:install git://github.com/joelvh/heroku-config.git
	heroku plugins:install git://github.com/heroku/heroku-pg-extras.git

setup-heroku-dev:
	heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
	yes | heroku bootstrap ${HEROKU_DEV_NAME}
	heroku labs:enable log-runtime-metrics
	heroku config:push -o --filename configs/env/common.env
	heroku config:push -o --filename configs/env/heroku.env
	heroku config:push -o --filename configs/env/secret.env
	heroku config:push -o --filename configs/env/dev.env
	heroku config:set 'heroku_app_'(heroku apps:info -s | grep '^name=')

setup-heroku-prod:
	heroku fork -a ${HEROKU_DEV_NAME} ${HEROKU_PROD_NAME}
	heroku labs:enable user-env-compile --app ${HEROKU_PROD_NAME}
	heroku labs:enable log-runtime-metrics --app ${HEROKU_PROD_NAME}
	heroku config:push -o --filename configs/env/prod.env --app ${HEROKU_PROD_NAME}
	heroku config:set 'heroku_app_'(heroku apps:info -s --app ${HEROKU_PROD_NAME} | grep '^name=') --app ${HEROKU_PROD_NAME}


reset-local:
	${MANAGE} clean_db --noinput
	${MANAGE} import_wp --traceback static/wordpress/.canada.wordpress.*
	${MANAGE} set_site 127.0.0.1:8000
	${MANAGE} loaddata configs/fixtures/contact.json

reset-heroku-dev:
	heroku pg:reset DATABASE_URL --confirm canada-development
	heroku run 'python manage.py clean_db --noinput'
	heroku run 'python manage.py import_wp  --traceback static/wordpress/.canada.wordpress.*'
	heroku run 'python manage.py set_site "$$heroku_app_name".herokuapp.com'
	heroku run 'python manage.py loaddata configs/fixtures/contact.json'

migrate-all:
	for app in (${MANAGE} syncdb | grep - | sed 's/ - //g');${MANAGE} schemamigration $$app --auto;end

migrate-wipe:
	rm -r {apps,libs}/*/migrations

migrate-init: migrate-wipe
	for app in (${MANAGE} syncdb | grep '^ . apps\|libs' | sed 's/ > //g' | sed 's/ - //g');${MANAGE} schemamigration $$app --initial;end

travis-encrypt:
	sed '/  global:/q' .travis.yml > .travis.yml.tmp
	mv -f .travis.yml.tmp .travis.yml
	cat configs/env/{common.env,secret.env} | travis encrypt --split --add

promote-db-local:
	pg_dump -Fc --no-acl --no-owner -h localhost -U saul django_canadanewyork > django_canadanewyork.dump
	${MANAGE} upload_file django_canadanewyork.dump > dump_url.txt
	rm django_canadanewyork.dump
	heroku pgbackups:restore DATABASE (cat dump_url.txt) --confirm ${HEROKU_DEV_NAME}
	rm dump_url.txt
	${MANAGE} delete_file django_canadanewyork.dump
	heroku run 'python manage.py set_site "$$heroku_app_name".herokuapp.com'

promote-db-heroku-dev:
	heroku pgbackups:transfer (heroku config:get DATABASE_URL --app ${HEROKU_PROD_NAME}) --app ${HEROKU_DEV_NAME}
	heroku run 'python manage.py set_site "$$heroku_app_name".herokuapp.com' --app ${HEROKU_PROD_NAME}

promote-code-local:
	git push heroku master
	yes | heroku bootstrap ${HEROKU_DEV_NAME}

promote-code-heroku-dev:
	heroku pipeline:promote
	yes | heroku bootstrap ${HEROKU_PROD_NAME}

promote-static-local:
	${MANAGE} clone_bucket (cat configs/env/dev.env | grep AWS_BUCKET | sed 's/AWS_BUCKET=//g') (heroku config:get AWS_BUCKET --app ${HEROKU_DEV_NAME})

promote-static-heroku-dev:
	${MANAGE} clone_bucket (heroku config:get AWS_BUCKET --app ${HEROKU_DEV_NAME}) (heroku config:get AWS_BUCKET --app ${HEROKU_PROD_NAME})

promote-all-local: promote-static-local promote-code-local promote-db-local

promote-all-heroku-dev: promote-static-heroku-dev promote-code-heroku-dev promote-db-heroku-dev
