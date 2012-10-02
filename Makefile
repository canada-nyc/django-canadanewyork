SHELL := /usr/local/bin/fish
heroku:
	heroku addons:add newrelic:standard
	heroku addons:add redistogo
	heroku addons:add memcachier:dev
	heroku addons:add heroku-postgresql:dev
	heroku labs:enable user-env-compile #enabled so that collectstatic has access to amazon ec2 key
	heroku config:add DJANGO_CONFIGURATION=ProductionSettings \
	                  SECRET_KEY='fa3rsdgaxczx' \
	                  AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
	                  AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
	                  AWS_STORAGE_BUCKET_NAME=canadanewyork \
	                  EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
	heroku pg:promote (heroku pg | grep '^===' | sed 's/^=== //g')
	git push heroku master:master
	heroku run 'python manage.py clean_db --no-wipe'
