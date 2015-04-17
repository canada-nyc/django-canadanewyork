web: newrelic-admin run-program gunicorn --log-file=- -c configs/gunicorn.py wsgi:application
worker: newrelic-admin run-program python manage.py pqworker

