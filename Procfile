web: fab sync;python canada/manage.py collectstatic --noinput;python canada/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3
worker: python canada/manage.py celeryd -E -B --loglevel=INFO
