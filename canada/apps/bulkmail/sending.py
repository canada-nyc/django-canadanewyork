import os

from rq import Queue
from redis.client import Redis

from django.core import mail
from django.template.loader import get_template
from django.template import Context


redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_connection = Redis.from_url(redis_url)
if True:
    async = True
else:
    async = False
q = Queue('email', connection=redis_connection, async=async)


def send_email(recipient, sender, subject, message):
            context = {
                'message': message,
                'recipient': recipient,
            }
            text_content = get_template('bulkmail/message.txt').render(Context(context))
            html_content = get_template('bulkmail/message.html').render(Context(context))
            msg = mail.EmailMultiAlternatives(subject, text_content, sender,
                                              to=[recipient.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
