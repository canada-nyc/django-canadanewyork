SHELL := /usr/local/bin/fish --login

PYTHON=/Users/saul/.virtualenvs/django-canadanewyork/bin/python
MANAGE=foreman run ${PYTHON} manage.py

HEROKU_DEV_NAME="canada-development"
HEROKU_PROD_NAME="canada"

ADDONS="blitz,pgbackups:auto-month,sentry,heroku-postgresql,newrelic,rediscloud,memcachier"

setup-local: setup-local-compression
	pip install -r configs/requirements/dev.txt
	mkdir tmp

setup-local-compression:
	# Install NPM if you don't have it installed
	# Tutorial on installing http://stackoverflow.com/questions/8986709/how-to-install-lessc-and-nodejs-in-a-python-virtualenv
	# On homebrew do `brew install nodejs`
	npm install --global --production "less" "git://github.com/mishoo/UglifyJS2.git#3bd7ca9961125b39dcd54d2182cb72bd1ca6006e"

setup-heroku:
	heroku plugins:install git://github.com/joelvh/heroku-config.git
	heroku plugins:install git://github.com/heroku/heroku-pg-extras.git

setup-heroku-dev:
	heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
	heroku create ${HEROKU_DEV_NAME} --addons ${ADDONS}
	heroku labs:enable log-runtime-metrics
	heroku config:push -o --filename configs/env/common.env
	heroku config:push -o --filename configs/env/heroku.env
	heroku config:push -o --filename configs/env/secret.env
	heroku config:push -o --filename configs/env/heroku-dev.env

setup-heroku-prod:
	heroku fork -a ${HEROKU_DEV_NAME} ${HEROKU_PROD_NAME}
	heroku labs:enable user-env-compile --app ${HEROKU_PROD_NAME}
	heroku addons:remove heroku-postgresql:dev -a ${HEROKU_PROD_NAME}
	heroku addons:add heroku-postgresql:crane -a ${HEROKU_PROD_NAME}
	heroku pg:promote (heroku pg --app ${HEROKU_PROD_NAME} | grep '^===' | sed 's/^=== //g') --app ${HEROKU_PROD_NAME}
	heroku config:push -o --filename configs/env/heroku-prod.env --app ${HEROKU_PROD_NAME}

reset-local:
	${MANAGE} clean_db --noinput
	${MANAGE} import_wp --traceback static/wordpress/.canada.wordpress.*

reset-heroku-dev:
	heroku pg:reset DATABASE_URL --confirm canada-development
	heroku run 'python manage.py clean_db --noinput'
	heroku run 'python manage.py import_wp  --traceback static/wordpress/.canada.wordpress.*'

migrate-all:
	for app in (${MANAGE} syncdb | grep - | sed 's/ - //g');${MANAGE} schemamigration $$app --auto;end

migrate-wipe:
	rm -r {apps,libs}/*/migrations

migrate-init: migrate-wipe
	for app in (${MANAGE} syncdb | grep '^ . apps\|libs' | sed 's/ > //g' | sed 's/ - //g');${MANAGE} schemamigration $$app --initial;end

promote-db-local:
	pg_dump -Fc --no-acl --no-owner -h localhost -U saul django_canadanewyork > django_canadanewyork.dump
	${MANAGE} upload_file django_canadanewyork.dump > dump_url.txt
	rm django_canadanewyork.dump
	heroku pgbackups:restore DATABASE (cat dump_url.txt) --confirm ${HEROKU_DEV_NAME}
	rm dump_url.txt
	${MANAGE} delete_file django_canadanewyork.dump
	heroku run 'python manage.py set_site "$$CANADA_ALLOWED_HOST"' -a ${HEROKU_DEV_NAME}

promote-db-heroku-dev:
	heroku pgbackups:capture -a ${HEROKU_DEV_NAME} --expire
	heroku pgbackups:restore DATABASE -a ${HEROKU_PROD_NAME} (heroku pgbackups:url -a ${HEROKU_DEV_NAME}) --confirm ${HEROKU_PROD_NAME}
	heroku run 'python manage.py set_site "$$CANADA_ALLOWED_HOST"' -a ${HEROKU_PROD_NAME}

demote-db-heroku-dev:
	heroku pgbackups:capture -a ${HEROKU_DEV_NAME}
	curl -o latest.dump (heroku pgbackups:url -a ${HEROKU_DEV_NAME})
	pg_restore --verbose --clean --no-acl --no-owner -h localhost -U saul -d django_canadanewyork latest.dump
	rm latest.dump

promote-code-local:
	heroku config:push -o --filename configs/env/common.env
	heroku config:push -o --filename configs/env/heroku.env
	heroku config:push -o --filename configs/env/secret.env
	heroku config:push -o --filename configs/env/heroku-dev.env
	git push heroku master
	heroku run python manage.py migrate

promote-code-heroku-dev:
	heroku config:push -o --filename configs/env/common.env --app ${HEROKU_PROD_NAME}
	heroku config:push -o --filename configs/env/heroku.env --app ${HEROKU_PROD_NAME}
	heroku config:push -o --filename configs/env/secret.env --app ${HEROKU_PROD_NAME}
	heroku config:push -o --filename configs/env/heroku-prod.env --app ${HEROKU_PROD_NAME}
	heroku pipeline:promote
	heroku run python manage.py migrate --app ${HEROKU_PROD_NAME}

promote-static-local:
	${MANAGE} clone_bucket $$AWS_BUCKET (heroku config:get AWS_BUCKET --app ${HEROKU_DEV_NAME})

promote-static-heroku-dev:
	${MANAGE} clone_bucket (heroku config:get AWS_BUCKET --app ${HEROKU_DEV_NAME}) (heroku config:get AWS_BUCKET --app ${HEROKU_PROD_NAME})

promote-all-local: promote-static-local promote-code-local promote-db-local

promote-all-heroku-dev: promote-static-heroku-dev promote-code-heroku-dev promote-db-heroku-dev
