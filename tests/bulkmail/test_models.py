from django.test import TestCase
from django.core import mail
from django_rq import get_worker


from canada.apps.bulkmail.admin import send_messages
from .factories import MessageFactory


class MessageTest(TestCase):
    def test_send_email(self):
        # Create message with 4 recipients
        message = MessageFactory(contact_list__contacts__n=4)
        # Send message via admin action
        #send_messages(queryset=[message])
        from django.core.mail import send_mail
        import django_rq
        django_rq.enqueue(send_mail, 'Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)
        # Proccesses job and then stops
        get_worker().work(burst=True)
        print mail.outbox

        # Test that 4 messages have been sent.
        self.assertEqual(len(mail.outbox), 4)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, message.subject)
