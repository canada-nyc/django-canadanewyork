import os

from rq import Queue
import redis

from django.core import mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_connection = redis.from_url(redis_url)
if settings.RQ:
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


def send_messages(modeladmin=None, request=None, queryset=None):
    connection = mail.get_connection()
    connection.open()
    for message in queryset:
        for recipient in message.contact_list.contacts.all():
            args = [recipient, 'gallery@canadanewyork.com', message.subject,
                      message.body]
            Queue('Email').enqueue(send_email, *args)
    connection.close()
