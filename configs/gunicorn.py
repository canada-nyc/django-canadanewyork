import os
import multiprocessing
try:
    workers = os.environ['GUNICORN_WORKERS']
except KeyError:
    workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30  # in seconds
