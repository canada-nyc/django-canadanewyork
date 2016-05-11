[![Build Status](https://next.travis-ci.org/saulshanabrook/django-canadanewyork.svg?branch=master)](https://next.travis-ci.org/saulshanabrook/django-canadanewyork)
[![Code Health](https://landscape.io/github/saulshanabrook/django-canadanewyork/master/landscape.svg?style=flat)](https://landscape.io/github/saulshanabrook/django-canadanewyork/master)
[![Requirements Status](https://requires.io/github/saulshanabrook/django-canadanewyork/requirements.png?branch=master)](https://requires.io/github/saulshanabrook/django-canadanewyork/requirements/?branch=master)
[![Dependency Status](https://gemnasium.com/saulshanabrook/django-canadanewyork.svg)](https://gemnasium.com/saulshanabrook/django-canadanewyork)


# Local
All local development is done through docker.



All runtime options are chosen using environmental variables.

For development, you should set a secret key and optionally admin credentials
if you want to create that:

```bash
echo 'app:
  environment:
    ADMIN_PASSWORD: password
    ADMIN_USERNAME: username
    SECRET_KEY: _
' > docker-compose.base.override.yml
```

To fill the database with test data and setup static:

```bash
docker-compose up -d db
docker-compose run --rm web python manage.py init_db 0.0.0.0:8000 --init
docker-compose run --rm web python manage.py collectstatic --noinput
```

To start the development server:

```bash
docker-compose up
open http://$(docker-machine ip default):8000
```

To run the tests:

```bash
docker-compose up -d db
docker-compose run --rm web python manage.py collectstatic --noinput
docker-compose run --rm -e CANADA_QUEUE_ASYNC=False web py.test
# or to run continiously use looponfail:
docker-compose run --rm -e CANADA_QUEUE_ASYNC=False web py.test -f
```

To make all migrations:

```bash
docker-compose run --rm web python manage.py makemigrations artists books custompages exhibitions photos press updates
```

To reset the local DB

```bash
docker-compose stop; docker-compose rm -f db data web worker; docker-compose up -d db; sleep 5; docker-compose run --rm web python manage.py init_db http://$(docker-machine ip default):8000/ --init; docker-compose run --rm web python manage.py collectstatic --noinput; docker-compose up web worker
```


## Static

To recompute the static files:


```bash
docker-compose -f docker-compose.static.yml run --rm less
docker-compose -f docker-compose.static.yml run --rm sass
```

# Transfering

## Database

To copy the DB from prod to staging:


```bash
heroku pg:copy canada::DATABASE_URL DATABASE_URL -a canada-development
```


And to copy to local environment:

```bash
docker-compose up -d db

bash -c 'env PATH=./bin/:$PATH dropdb postgres'

# don't worry that this will fail halfway through, just cant verify DB
bash -c 'env PATH=./bin/:$PATH heroku pg:pull DATABASE_URL postgres --app canada'
```

## Configuration

### Pulling

To then to run locally with env variables from production

```bash
heroku config:pull --overwrite --env docker-compose.env -a canada
echo 'CANADA_ALLOWED_HOST=*' >> docker-compose.env
docker-compose up web
```

### Pushing
To push the `app.json` variables to an existing heroku app:


```bash
jq '.env | with_entries(select(.value | type == "string")) | to_entries | map("\(.key)=\(.value)") | join("\n")' -r app.json  > .env
heroku config:push --overwrite -a <app name>
```

## Static

To replace the development static media assets (which are shared accross
all development apps) with the production ones:

```bash
heroku run python manage.py clone_bucket assets.canadanewyork.com assets-dev.canadanewyork.com -a canada-development
```

You can run that command anywhere you have set up S3 with the proper credentials
as the storage backend.
