SHELL := /usr/local/bin/fish

local-setup:
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

HEROKU_ADDONS="newrelic,redistogo,heroku-postgresql,pgbackups,MEMCACHIER,sentry"

heroku-setup-dev:
	heroku plugins:install git://github.com/joelvh/heroku-config.git
	heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
	heroku apps:create canada-development --addons $HEROKU_ADDONS
	heroku config:push -o --filename configs/env/common.env
	heroku config:push -o --filename configs/env/heroku.env
	heroku config:push -o --filename configs/env/secret.env
	heroku config:push -o --filename configs/env/dev.env
	heroku config:set 'heroku_app_'(heroku apps:info -s | grep '^name=')

heroku-setup-prod:
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

heroku-promote-db:
	heroku pgbackups:capture --expire --app canada-development
	heroku pgbackups:restore DATABASE --app canada (heroku pgbackups:url --app canada-development) --confirm canada
	heroku run 'python manage.py set_site "$heroku_app_name".herokuapps.com' --app canada

heroku-promote-code:
	heroku pipeline:promote

heroku-promote-static:
	heroku run 'python manage.py clone_bucket (heroku config:get AWS_BUCKET --app canada-development) (heroku config:get AWS_BUCKET canada)'

heroku-promote-all: heroku-promote-static heroku-promote-code heroku-promote-db

heroku-reset-dev:
	heroku pg:reset DATABASE_URL --confirm canada-development
	heroku run 'python manage.py clean_db --noinput'
	heroku run 'python manage.py import_wp static/wordpress/.canada.wordpress.*'
	heroku run 'python manage.py set_site "$heroku_app_name".herokuapps.com'
	foreman run python manage.py loaddata configs/fixtures/contact.json
