import django_rq

from django.contrib import admin

from .models import ContactList, Contact, Message
from .sending import send_email


def send_messages(modeladmin=None, request=None, queryset=None):
    for message in queryset:
        for recipient in message.contact_list.contacts.all():
            host = request.get_host() if request else 'localhost'
            args = [recipient, 'gallery@canadanewyork.com', message,
                   host]
            django_rq.enqueue(send_email, *args)


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
