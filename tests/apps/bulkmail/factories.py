import factory

from canada.apps.bulkmail.models import Message, ContactList, Contact
from ...functions import django_image
from ...factories import DjangoFactory


class ContactListFactory(DjangoFactory):
    FACTORY_FOR = ContactList

    name = factory.Sequence(lambda n: 'Contact List {}'.format(n))

    @factory.post_generation(extract_prefix='contacts')
    def create_contacts(self, create, extracted, **kwargs):
        # ContactListFactory(contacts=[<contact1>, ...])
        if extracted:
            [ContactFactory(contact_list=self) for contact in extracted]
        # ContactListFacotry(contacts__n=3)
        elif 'n' in kwargs:
            [ContactFactory(contact_list=self) for _ in range(int(kwargs['n']))]
        # ContactListFacotry()
        else:
            ContactFactory(contact_list=self)


class ContactFactory(DjangoFactory):
    FACTORY_FOR = Contact

    email = factory.Sequence(lambda n: '{}@example.com'.format(n))
    contact_list = factory.SubFactory(ContactListFactory)


class MessageFactory(DjangoFactory):
    FACTORY_FOR = Message

    subject = factory.Sequence(lambda n: 'Subject {}'.format(n))
    body = factory.LazyAttribute(lambda a: '{} message'.format(a.subject))
    image = factory.LazyAttribute(lambda a: django_image(a.subject))
    contact_list = factory.SubFactory(ContactListFactory)
