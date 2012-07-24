import requests

from django.contrib import admin
from django.core import mail
from django.template.loader import get_template
from django.template import Context

from .models import ContactList, Contact, Message
from ..admin import image_file


def send_messages(self, request, queryset):
    connection = mail.get_connection()
    connection.open()
    q = Queue('Email')
    for message in queryset:
        q.enqueue(send_email,
                  message.contact_list.contacts.all(),
                  'gallery@canadanewyork.com',
                  'bulkmail/message.txt',
                  'bulkmail/message.html',
                  message.subject,
                  message)
    connection.close()


def send_email(recipients, from, text_template, html_template, subject, message):
    for recipient in recipients:
            context = {
                'message': message,
                'recipient': recipient,
            }
            text_content = get_template(text_template).render(Context(context))
            html_content = get_template(html_template).render(Context(context))
            msg = mail.EmailMultiAlternatives(subject, text_content, from,
                                              to=[recipient.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'contact_list')


class ContactInline(admin.TabularInline):
    model = Contact


class ContactListAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    list_display = ('name', 'default')


class MessageAdmin(admin.ModelAdmin):
    actions = [send_messages]
    list_display = ('image_thumb', 'subject', 'contact_list', 'date_time')
    list_filter = ('contact_list',)
    image_thumb = image_file('obj.image')

admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactList, ContactListAdmin)
admin.site.register(Message, MessageAdmin)
