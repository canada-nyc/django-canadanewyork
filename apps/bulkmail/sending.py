from django.core import mail
from django.template.loader import get_template
from django.template import Context

import django_rq

from .worker_control import Worker


def send_email(recipient_model, sender_email, message_model, domain):
    _Worker = Worker()
    _Queue = django_rq.get_queue()
    _Worker.scale(1)
    context = {
        'message': message_model,
        'recipient': recipient_model,
        'domain': domain,
    }
    text_content = get_template('bulkmail/message.txt').render(Context(context))
    html_content = get_template('bulkmail/message.html').render(Context(context))
    msg = mail.EmailMultiAlternatives(message_model.subject,
                                      text_content,
                                      sender_email,
                                      to=[recipient_model.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    if _Queue.is_empty():
        _Worker.scale(0)
