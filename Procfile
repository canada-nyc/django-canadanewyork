web: python manage.py collectstatic --noinput --verbosity 0; newrelic-admin run-program gunicorn -c configs/gunicorn.py wsgi:application
worker: python manage.py pqworker
