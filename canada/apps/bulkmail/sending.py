from django.core import mail
from django.template.loader import get_template
from django.template import Context


def send_email(recipient_model, sender_email, message_model, domain):
            context = {
                'message': message_model,
                'recipient': recipient_model,
                'domain': domain,
            }
            text_content = get_template('bulkmail/message.txt').render(Context(context))
            html_content = get_template('bulkmail/message.html').render(Context(context))
            msg = mail.EmailMultiAlternatives(message_model.subject,
                                              text_content,
                                              message_model,
                                              to=[recipient_model.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
