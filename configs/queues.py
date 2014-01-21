from pq.queue import Queue
from django.conf import settings
from django.db import DatabaseError


queue = Queue.create(async=settings.QUEUE_ASYNC)

# Try to create the queue table, but if the database isn't set up yet
# then don't create it
try:
    queue.save()
except DatabaseError:
    pass
