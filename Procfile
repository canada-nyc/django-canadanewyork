web: python manage.py collectstatic --noinput; gunicorn -c configs/gunicorn.py wsgi:application
worker: python manage.py pqworker

