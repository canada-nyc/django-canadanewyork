import factory

from canada.apps.bulkmail.models import Message, ContactList, Contact


class MessageFactory(factory.Factory):
    import datetime
    FACTORY_FOR = Message

    date_time = datetime.now()
    subject = factory.LazyAttributeSequence(lambda _, n: 'Subject {}'.format(n))
    body = factory.LazyAttribute(lambda a: '{} message'.format(a.subject))
    image = factory.SubFactory(ConctactListFactory)
    contact_list = factory.SubFactory(ConctactListFactory)


class ContactListFactory(factory.Factory):
    FACTORY_FOR = ContactList

    name = factory.LazyAttributeSequence(lambda _, n: 'Contact List {}'.format(n))
    default = False
    contact = factory.RelatedFactory(ContactFactory, 'contact_list')


class ContactFactory(factory.Factory):
    FACTORY_FOR = Contact

    email = factory.LazyAttributeSequence(lambda _, n: '{}@example.com'.format(n))
    contact_list = factory.SubFactory(ConctactListFactory)
