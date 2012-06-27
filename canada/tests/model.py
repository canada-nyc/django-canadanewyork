from django.test import TestCase
from django.template.defaultfilters import slugify

import factory

from canada.bulkmail.models import ContactList, Message


class ContactListFactory(factory.Factory):
    FACTORY_FOR = ContactList

    name = factory.Sequence(lambda n: 'list{}'.format(n))


class ContactListTest(TestCase):
    def setUp(self):
        self.contactlist = ContactList.build()

    def tearDown(self):
        self.contactlist.delete()

    def test_(self):
        self.artist.save()
        self.assertEqual(self.artist.slug,
                         slugify('-'.join([self.first_name, self.last_name]))

        self.assertEqual(self.user_one.slug, slugify(self.user_one.username))

    def test_last_letter_recipients(self):
        # No letters should return false
        self.assertFalse(self.user_two.last_letter_recipients)
        # Return user(s) shared in last letter
        self.assertEqual(self.user_one.last_letter_recipients, [self.user_two])
