from rq import Queue

from django.contrib import admin
from django.core import mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from .models import ContactList, Contact, Message


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
            if  settings.RQ != False:
                Queue('Email').enqueue(send_email, *args)
            else:
                send_email(*args)
    connection.close()


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'contact_list')


class ContactInline(admin.TabularInline):
    model = Contact


class ContactListAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    list_display = ('name', 'default')


class MessageAdmin(admin.ModelAdmin):
    actions = [send_messages]
    list_display = ('subject', 'contact_list', 'date_time')
    list_filter = ('contact_list',)

admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactList, ContactListAdmin)
admin.site.register(Message, MessageAdmin)
