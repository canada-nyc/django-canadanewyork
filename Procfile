web: python manage.py collectstatic --noinput; newrelic-admin run-program gunicorn -c configs/gunicorn.py wsgi:application
worker: python manage.py pqworker

