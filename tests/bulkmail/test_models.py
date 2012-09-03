from django.test import TestCase
from django.core import mail
from django.test.utils import override_settings

from canada.apps.bulkmail import admin
from .factories import MessageFactory


#@override_settings(RQ=False)
class MessageTest(TestCase):
    def test_send_email(self):
        # Create message with 4 recipients
        message = MessageFactory(contact_list__contacts__n=4)
        # Send message via admin action
        admin.send_messages(queryset=[message])

        # Test that 4 messages have been sent.
        self.assertEqual(len(mail.outbox), 4)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, message.subject)
