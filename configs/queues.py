from pq.queue import Queue
from django.conf import settings

queue = Queue.create(async=settings.QUEUE_ASYNC)
queue.save()

enqueue = queue.enqueue
