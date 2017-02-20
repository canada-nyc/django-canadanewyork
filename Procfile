web: gunicorn --log-file=- -c configs/gunicorn.py wsgi:application
worker: celery -A configs worker -l info
