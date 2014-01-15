from pq.queue import Queue
from django.conf import settings

print settings.QUEUE_ASYNC
queue = Queue.create(async=settings.QUEUE_ASYNC)

enqueue = queue.enqueue
