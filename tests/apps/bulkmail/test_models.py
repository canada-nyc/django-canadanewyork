from django.test import TestCase
from django_rq import get_worker


from apps.bulkmail.admin import send_messages
from .factories import MessageFactory


class MessageTest(TestCase):
    def test_send_email(self):
        # Create message with 4 recipients
        message = MessageFactory(contact_list__contacts__n=4)
        # Send message via admin action
        send_messages(queryset=[message])
        # Proccesses job and then stops
        get_worker().work(burst=True)
